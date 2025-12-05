# PDF Chatbot — RAG-Based Document Question Answering

A smart chatbot system that enables users to **upload PDFs** and ask questions based on their content.
It uses a **Retrieval-Augmented Generation (RAG)** workflow to return **factual** and **grounded directly in the PDF content**.

---

## Features

✔ Upload any PDF document via UI
✔ Automatic text extraction and intelligent chunking
✔ Embeddings using Sentence Transformers
✔ FAISS vector search for fast and accurate retrieval
✔ Ask natural-language questions
✔ Context-aware answers powered by an LLM (Ollama)
✔ Streamlit-based frontend and FastAPI backend
✔ Fully containerized using Docker

---

## System Architecture

```
  User
   │
   ▼
Frontend (Streamlit)
   │  ├── Upload PDF
   │  └── Ask Questions
   ▼
Backend (FastAPI)
   │  ├── PDF Text Extraction
   │  ├── Text Chunking
   │  ├── Embedding Generation
   │  └── FAISS Vector Search
   ▼
LLM (Ollama - llama3.1:8b)
   └── Final Answer Generation
```

---

## Tech Stack

| Component   | Technology            |
| ----------- | --------------------- |
| Frontend UI | Streamlit             |
| API         | FastAPI               |
| Vector DB   | FAISS                 |
| Embeddings  | Sentence Transformers |
| LLM         | Ollama                |
| Packaging   | Docker                |
| Language    | Python                |

---

## RAG Pipeline

1️⃣ Upload a PDF 
2️⃣ Extract full document text page wise
3️⃣ Split text into overlapping chunks
4️⃣ Convert chunks → vector embeddings
5️⃣ Store in FAISS index
6️⃣ Query → Retrieve relevant chunks
7️⃣ Feed context into LLM → Final answer

Result: **Trustworthy answers grounded in source content**

---

## Project Structure

```
pdf_chatbot/
│
├── backend/
│ ├── routes/
│ │ └── ask_route.py # Main chatbot endpoint
│ ├── services/
│ │ ├── extract_text.py
│ │ ├── chunk_text.py
│ │ ├── embeddings.py
│ │ ├── faiss_store.py
│ │ └── faiss_query.py
│ └── data/
│ │  ├── uploads/
│ │  ├── chunks/
│ │  └── faiss_indexes/
│ └── requirements.txt
│
├── frontend/
│ ├── Dockerfile # Frontend container
│ ├── requirements.txt
│ └── app.py # Streamlit app
│  
├── main.py # FastAPI entrypoint
├── config.py
├── Dockerfile # Backend container
├── docker-compose.yml # Full stack
└── README.md
```

---

## How to Run

### Option 1 — Run using Docker (Recommended)

Make sure Docker Desktop is running.

```bash
docker-compose up


Once services are up:

| Service      |           URL                 |
| ------------ | ------------------------------|
| Streamlit UI |   http://localhost:8501       |
| FastAPI Root |   http://localhost:8000       |
| API Docs     |   http://localhost:8000/docs  |


## Option 2 — Run Locally (Dev Mode)

### Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 2️⃣ Install Dependencies

Backend:

cd backend
pip install -r requirements.txt
cd ..


Frontend:

cd frontend
pip install -r requirements.txt
cd ..

### Start Backend (FastAPI)

```bash
uvicorn main:app --reload --port 8000
```

### Start Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

---

## API Overview

| Endpoint      | Method | Input               | Output                    | Description                     |
| ------------- | ------ | ------------------- | ------------------------- | ------------------------------- |
| `/upload-doc` | POST   | PDF file            | `doc_id`                  | Upload & process PDF Documents  |
| `/ask`        | POST   | `{ doc_id, query }` | Answer + retrieved chunks | RAG-based QA                    |

---

## Models

| Component         | Purpose                                                          |
| ----------------- | ---------------------------------------------------------------- |
| all-MiniLM-L6-v2  | Lightweight embedding model for CPU-friendly semantic similarity |
| FAISS IndexFlatL2 | Efficient vector search based on cosine similarity               |
| llama3.1:8b model | Query + retrieved context used to generate final grounded answer |

---

## Author

Muhammad Ali Nawaz Malik
AI / Machine Learning Developer — Islamabad, Pakistan


