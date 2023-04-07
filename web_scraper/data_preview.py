import json
import random

def read_poems(file_path, num_poems=5):
    with open(file_path, 'r') as f:
        poems = json.load(f)

    # Get random poem IDs
    poem_ids = random.sample(list(poems.keys()), num_poems)

    # Print poems
    for poem_id in poem_ids:
        poem = poems[poem_id]
        print(f"ID: {poem_id}")
        print(f"Title: {poem['title']}")
        print(f"Poet: {poem['poet']}")
        print(f"Tags: {poem['tags']}")
        print(f"Poem:\n{poem['poem']}\n")
        input()
        
if __name__ == '__main__':
    read_poems('poetry_foundation_poems.json', 5)