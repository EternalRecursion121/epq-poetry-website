from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from inference import predict_mask

with open("data/poems.json") as f:
    poems = json.load(f)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/mask-suggestions")
def get_mask_suggestions(poem_str):
    return predict_mask(poem_str)
