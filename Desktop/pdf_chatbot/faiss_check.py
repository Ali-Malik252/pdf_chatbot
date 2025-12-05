# import faiss
# print(faiss.__version__)
import numpy as np
import faiss
from pathlib import Path

# ------------------------------
# CONFIG: update these paths
# ------------------------------
CHUNK_FOLDER = Path("C:/Users/hp/Desktop/pdf_chatbot/backend/data/chunks")
FAISS_FOLDER = Path("C:/Users/hp/Desktop/pdf_chatbot/backend/data/faiss_indexes")

# Replace with your doc_id
doc_id = "38738cfd-5738-4008-8389-a383fa94c2a1"

# ------------------------------
# Load embeddings
# ------------------------------
embedding_file = CHUNK_FOLDER / f"{doc_id}_embeddings.npy"
embeddings = np.load(embedding_file)

print(f"Loaded embeddings from {embedding_file}")
print(f"Shape: {embeddings.shape}")
print(f"First embedding vector:\n{embeddings[0]}")

# ------------------------------
# Load FAISS index
# ------------------------------
faiss_file = FAISS_FOLDER / f"{doc_id}_index.faiss"
index = faiss.read_index(str(faiss_file))

print(f"\nLoaded FAISS index from {faiss_file}")
print(f"Number of vectors in index: {index.ntotal}")

# ------------------------------
# Test a similarity search
# ------------------------------
k = 2  # top-k results
D, I = index.search(embeddings[0:1], k)  # search using first vector as query

print(f"\nTop {k} nearest neighbors for first vector:")
for rank, (idx, dist) in enumerate(zip(I[0], D[0]), start=1):
    print(f"{rank}. Chunk index: {idx}, Distance: {dist}")
