import json

with open('ids.json') as f:
    ids = json.load(f)
    print(len(ids))