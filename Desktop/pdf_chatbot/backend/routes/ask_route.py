import sys
import os
import json
import faiss
import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# --------------------------------------------------
# Add project root to PYTHONPATH
# --------------------------------------------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import FAISS_FOLDER, CHUNK_FOLDER
from backend.services.embeddings import generate_embeddings

# Correct Ollama import
import ollama

router = APIRouter()


# --------------------------------------------------
# Request body schema
# --------------------------------------------------
class AskRequest(BaseModel):
    doc_id: str
    query: str
    top_k: int = 2


# --------------------------------------------------
# Chatbot API — /ask endpoint
# --------------------------------------------------
@router.post("/ask")
async def ask_question(request: AskRequest):
    doc_id = request.doc_id
    query = request.query
    top_k = request.top_k

    # --------------------------------------------------
    # Step 1 — Load FAISS index
    # --------------------------------------------------
    faiss_path = FAISS_FOLDER / f"{doc_id}_index.faiss"

    if not faiss_path.exists():
        raise HTTPException(status_code=404, detail="FAISS index not found.")

    index = faiss.read_index(str(faiss_path))

    # --------------------------------------------------
    # Step 2 — Load chunks
    # --------------------------------------------------
    chunk_path = CHUNK_FOLDER / f"{doc_id}_chunks.json"

    if not chunk_path.exists():
        raise HTTPException(status_code=404, detail="Chunk file not found.")

    with open(chunk_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # --------------------------------------------------
    # Step 3 — Embed query
    # --------------------------------------------------
    query_vec = generate_embeddings([query]).astype(np.float32)

    # --------------------------------------------------
    # Step 4 — Search FAISS
    # --------------------------------------------------
    distances, indices = index.search(query_vec, top_k)

    retrieved_chunks = [
        chunks[i] for i in indices[0] if i < len(chunks)
    ]

    # --------------------------------------------------
    # Step 5 — Build context
    # --------------------------------------------------
    context_text = "\n\n".join(chunk["text"] for chunk in retrieved_chunks)

    # --------------------------------------------------
    # Step 6 — Ask Ollama (correct usage)
    # --------------------------------------------------
    prompt = f"""
    Use ONLY the following context to answer the question.

    Context:
    {context_text}

    Question: {query}

    Answer:
    """

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response["message"]["content"]

    # --------------------------------------------------
    # Step 7 — Return final JSON
    # --------------------------------------------------
    return {
        "doc_id": doc_id,
        "query": query,
        "answer": answer,
        "retrieved_chunks": retrieved_chunks
    }
