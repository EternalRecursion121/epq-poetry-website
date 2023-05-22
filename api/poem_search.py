import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the poems from JSON file
def load_db():
    with open('poems_database.json', 'r') as f:
        db = json.load(f)
    return list(db.values()) 

# Prepare the embeddings of the poems
def prepare_poems():
    poems = load_db()
    poem_embeddings = []
    
    for poem_obj in poems:
        text_to_encode = poem_obj['title'] + "|" + poem_obj['poem']
        poem_embedding = model.encode(text_to_encode)
        poem_embeddings.append(poem_embedding)
        
    poem_embeddings = np.array(poem_embeddings, dtype='float32')

    # Normalize the embeddings to use cosine similarity in faiss
    faiss.normalize_L2(poem_embeddings)
    return poems, poem_embeddings

# Create and save the FAISS index
def create_index():
    poems, poem_embeddings = prepare_poems()
    index = faiss.IndexFlatIP(poem_embeddings.shape[1])
    index.add(poem_embeddings)
    faiss.write_index(index, 'db.index')

# Create query embedding
def create_query_embedding(query):
    query_embedding = model.encode([query])
    # Normalize the embedding to use cosine similarity in faiss
    faiss.normalize_L2(query_embedding)
    return query_embedding

# Find similar poems in the database
def find_similar_poems(query, n=5):
    # Get query embedding and search in the index
    D, I = index.search(create_query_embedding(query), n)

    # Get the info for each similar poem
    similar_poems = [db[i] for i in I[0]]

    return D[0], similar_poems

# Load the index
index = faiss.read_index('db.index')
db = load_db()

print(index.ntotal, "poems loaded.")

if __name__=="__main__":
    # Create index if not already created
    create_index()

    # Sample query
    query = """Do not go gentle into that good night,
    Old age should burn and rave at close of day;
    Rage, rage against the dying of the light.
    """

    distances, similar_poems = find_similar_poems(query)

    print(similar_poems[0])
    print(distances[0])

    query = """The sun sets across the horizon,
    As the whispering wind rustles through the trees,
    The river flows with a silent majesty,
    Nature's beauty is a sight to appease.
    """

    # Measure performance
    import time
    start = time.time()
    for distance, poem in zip(*find_similar_poems(query)):
        print(poem['title'], f"Distance: {distance}")
        print(poem['poem'][:100], "...")

    end = time.time()
    print("Time taken: ", (end-start)/1000, "seconds")

