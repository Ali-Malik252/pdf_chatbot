import faiss
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import FAISS_FOLDER, CHUNK_FOLDER

# Load the same model used during embedding creation
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def search_faiss(doc_id: str, question: str, k: int = 2):
    """
    Search the FAISS index for a specific document
    and return the top-k most relevant chunks.

    Args:
        doc_id (str): Document ID
        question (str): User question
        k (int): Number of results to retrieve

    Returns:
        List[Dict]: Retrieved chunks (with text + metadata)
    """

    # -------------------------------------------
    # 1. Load FAISS index from FAISS_FOLDER
    # -------------------------------------------
    index_path = FAISS_FOLDER / f"{doc_id}_index.faiss"

    if not index_path.exists():
        raise FileNotFoundError(f"FAISS index not found for doc_id: {doc_id}")

    index = faiss.read_index(str(index_path))

    # -------------------------------------------
    # 2. Load chunks JSON from CHUNK_FOLDER
    # -------------------------------------------
    chunk_file_path = CHUNK_FOLDER / f"{doc_id}_chunks.json"

    if not chunk_file_path.exists():
        raise FileNotFoundError(f"Chunks JSON file missing for doc_id: {doc_id}")

    with open(chunk_file_path, "r", encoding="utf-8") as f:
        chunks_data = json.load(f)

    # -------------------------------------------
    # 3. Encode the question into an embedding
    # -------------------------------------------
    query_vector = model.encode([question]).astype("float32")

    # -------------------------------------------
    # 4. Search FAISS index
    # -------------------------------------------
    distances, indices = index.search(query_vector, k)

    # -------------------------------------------
    # 5. Collect matching chunks
    # -------------------------------------------
    results = []
    for idx in indices[0]:
        if idx < len(chunks_data):
            results.append(chunks_data[idx])

    return results
