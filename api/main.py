from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp, Scope
from datetime import datetime
import json
import requests
from inference import predict_mask, predict_mask_multi
from gpt_commands import feedback, generate_metaphor, rewrite_line
import logging

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

with open("data/poems.json") as f:
    poems = json.load(f)

origins = [
    "http://localhost:5173",
    "https://epq-poetry-website.vercel.app",
    "https://7d52-51-182-252-33.ngrok-free.app"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = datetime.utcnow()
        logging.info(f"--- Request {request.method} {request.url} started at {start_time.isoformat()} ---")

        response = await call_next(request)
        process_time = datetime.utcnow() - start_time

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        response_clone = Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

        logging.info(f"--- Response body: {response_clone.body.decode()} took {process_time.total_seconds()} seconds ---")

        async def streaming_body() -> None:
            yield response_body
        response.body_iterator = streaming_body()
        return response

app.add_middleware(LoggingMiddleware)


def save_poems():
    with open("data/poems.json", "w") as f:
        json.dump(poems, f)

@app.get("/poems")
def get_poems():
    return poems

@app.get("/poems/{poem_id}")
def get_poem(poem_id: str):
    if poem_id not in poems:
        raise HTTPException(status_code=404, detail="Poem not found")
    return {"id": poem_id, "poem": poems[poem_id]}

@app.post("/poems")
def add_poem(poem: dict):
    poem_id = str(max(map(int, poems.keys()), default=0) + 1)
    poems[poem_id] = poem
    save_poems()
    return {"poem_id": poem_id, "poem": poem}

@app.put("/poems/{poem_id}")
def update_poem(poem_id: str, poem: dict):
    if poem_id not in poems:
        raise HTTPException(status_code=404, detail="Poem not found")
    poems[poem_id] = poem
    save_poems()
    return {"poem_id": poem_id, "poem": poem}

@app.delete("/poems/{poem_id}")
def delete_poem(poem_id: str):
    if poem_id not in poems:
        raise HTTPException(status_code=404, detail="Poem not found")
    del poems[poem_id]
    save_poems()
    return {"poem_id": poem_id}

@app.post("/suggest_replacement")
def suggest_replacement(data: dict):
    print(data["poem_str"])
    return {"suggestions": predict_mask(data["poem_str"])}

@app.post("/suggest_replacement_multi")
def suggest_replacement_multi(data: dict):
    return {"suggestions": predict_mask_multi(data["poem_str"])}

@app.get("/synonyms")
def get_synonyms(word: str, lc: str = None, rc: str = None):
    req_url = f"https://api.datamuse.com/words?rel_syn={word}"
    if lc:
        req_url += f"&lc={lc}"
    if rc:
        req_url += f"&rc={rc}"
    response = requests.get(req_url)
    return response.json()[:5]

@app.get("/rhymes")
def get_rhymes(word: str, lc: str = None, rc: str = None):
    req_url = f"https://api.datamuse.com/words?rel_rhy={word}"
    if lc:
        req_url += f"&lc={lc}"
    if rc:
        req_url += f"&rc={rc}"
    response = requests.get(req_url)
    return response.json()[:5]

@app.post("/feedback")
def get_feedback(poem: dict):
    return {"feedback": feedback(poem)}

@app.post("/metaphors")
def get_generate_metaphor(data: dict):
    return {"metaphors": generate_metaphor(data["poem"], data["source"], data["target"])}

@app.post("/rewrite_line")
def get_rewrite_line(data: dict):
    return {"rewrite": rewrite_line(data["poem"], data["line"])}