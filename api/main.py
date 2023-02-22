from fastapi import FastAPI, HTTPException
import json

with open("data/poems.json") as f:
    poems = json.load(f)

app = FastAPI()

def save_poems():
    with open("data/poems.json", "w") as f:
        json.dump(poems, f)

@app.get("/poems")
def get_poems():
    print("HI")
    return poems

@app.get("/poems/{poem_id}")
def get_poem(poem_id: int):
    if poem_id not in poems:
        raise HTTPException(status_code=404, detail="Poem not found")
    return {"poem_id": poem_id, "poem": poems[poem_id]}

@app.post("/poems")
def add_poem(poem: dict):
    poem_id = max(poems.keys()) + 1
    poems[poem_id] = poem
    save_poems()
    return {"poem_id": poem_id, "poem": poem}

@app.put("/poems/{poem_id}")
def update_poem(poem_id: int, poem: dict):
    if poem_id not in poems:
        raise HTTPException(status_code=404, detail="Poem not found")
    poems[poem_id] = poem
    save_poems()
    return {"poem_id": poem_id, "poem": poem}

@app.delete("/poems/{poem_id}")
def delete_poem(poem_id: int):
    if poem_id not in poems:
        raise HTTPException(status_code=404, detail="Poem not found")
    del poems[poem_id]
    save_poems()
    return {"poem_id": poem_id}



