import json
import random

def read_poems_poetry_foundation(num_poems=5):
    with open('poetry_foundation_poems.json', 'r') as f:
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

def read_poems_poets(num_poems=5):
    with open('poetsorg_poems_unique.json', 'r') as f:
        poems = json.load(f)

    print(len(poems))

    ## Remove dupplicates
    unique =  set(map(lambda x: tuple(x.values()), poems))

    poems = [dict(zip(poems[0].keys(), values)) for values in unique]
    
    

    ## Save unique poems

    with open('poetsorg_poems_unique.json', 'w') as f:
        json.dump(poems, f)


    # with open('poetsorg_poems.json', 'w') as f:
    #     json.dump(poems, f)

    # # Get random poem IDs
    # poems = random.sample(poems, num_poems)

    # # Print poems
    # for poem in poems:
    #     for key, value in poem.items():
    #         print(f"{key}: {value}")
    #     input()
        
if __name__ == '__main__':
    read_poems_poets(5)