from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import re
import os

# Initialize paths
current_dir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(current_dir, "faiss_index.faiss")
metadata_path = os.path.join(current_dir, "chunk_metadata.json")

# Load model and index
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(index_path)

# Load metadata
with open(metadata_path, "r") as f:
    metadata = json.load(f)

def clean(text):
    text = text.replace("\n", " ").replace("\t", " ")
    text = re.sub(" +", " ", text)
    return text.strip()

def retrieve_similar(query, top_k=5):
    query_vector = model.encode([query], normalize_embeddings=True).astype("float32")
    distances, indices = index.search(query_vector, top_k)
    return [clean(metadata[idx]["text"]) for idx in indices[0] if idx < len(metadata)]