from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from inference import predict_mask, predict_mask_multi
import requests

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

@app.post("/suggest_replacement")
def suggest_replacement(data: dict):
    print(data["poem_str"])
    return {"suggestions": predict_mask(data["poem_str"])}

@app.post("/suggest_replacement_multi")
def suggest_replacement_multi(data: dict):
    return {"suggestions": predict_mask_multi(data["poem_str"])}

@app.get("/synonyms/{word}")
def get_synonyms(word: str):
    response = requests.get(f"https://api.datamuse.com/words?rel_syn={word}")
    return response.json()

@app.get("/rhymes/{word}")
def get_rhymes(word: str):
    response = requests.get(f"https://api.datamuse.com/words?rel_rhy={word}")
    return response.json()

