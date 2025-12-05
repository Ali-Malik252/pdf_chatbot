# FOR CONTAINERIZATION - DOCKER

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import json
import numpy as np

# Import services
from backend.services.extract_text import extract_text_from_pdf
from backend.services.chunk_text import create_text_chunks
from backend.services.embeddings import generate_embeddings
from backend.services.faiss_store import create_faiss_index

# Config paths
from config import UPLOAD_FOLDER, CHUNK_FOLDER

# Import routes
from backend.routes.ask_route import router as ask_router

# -----------------------------
# FastAPI app initialization
# -----------------------------
app = FastAPI(title="PDF Chatbot API", description="RAG-based document question answering")

# -----------------------------
# CORS Middleware
# -----------------------------
# Allow frontend container to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router for /ask endpoint
app.include_router(ask_router)

# -----------------------------
# Root endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

# -----------------------------
# Document upload endpoint
# -----------------------------
@app.post("/upload-doc")
async def document_upload(file: UploadFile = File(...)):
    """
    Accepts a PDF, saves it, extracts text, chunks text,
    generates embeddings, creates FAISS index, returns doc_id.
    """
    # Validate file type
    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are allowed."})

    # Generate unique document ID
    doc_id = str(uuid.uuid4())

    # Save PDF
    pdf_path = UPLOAD_FOLDER / f"{doc_id}.pdf"
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # Extract text from PDF
    pages_text = extract_text_from_pdf(pdf_path)

    # Optional: save extracted text for reference
    text_save_path = UPLOAD_FOLDER / f"{doc_id}_text.txt"
    with open(text_save_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(pages_text))

    # Split text into chunks
    chunks = create_text_chunks(doc_id, pages_text)

    # Save chunks JSON
    chunk_file_path = CHUNK_FOLDER / f"{doc_id}_chunks.json"
    with open(chunk_file_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    # Generate embeddings for chunks
    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)  # returns numpy array

    # Save embeddings
    embedding_file_path = CHUNK_FOLDER / f"{doc_id}_embeddings.npy"
    np.save(embedding_file_path, embeddings)

    # Create FAISS index
    faiss_file_path = create_faiss_index(doc_id, embedding_file_path)

    # Return response
    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "num_pages": len(pages_text),
        "num_chunks": len(chunks),
        "faiss_index": str(faiss_file_path)
    }


from config import UPLOAD_FOLDER, CHUNK_FOLDER, FAISS_FOLDER
print("Upload folder:", UPLOAD_FOLDER)
print("Chunk folder:", CHUNK_FOLDER)
print("FAISS folder:", FAISS_FOLDER)
