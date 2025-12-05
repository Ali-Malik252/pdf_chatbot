# PDF Chatbot — RAG-Based Document Question Answering

A smart chatbot system that enables users to upload PDF documents and ask questions based on their content.
It uses a **Retrieval-Augmented Generation (RAG)** workflow to return **accurate and context-aware** answers directly sourced from the document.

---

## Features

✔ Upload PDF documents
✔ Automatic text extraction
✔ Intelligent text chunking
✔ FAISS vector storage & retrieval
✔ Ask natural-language questions
✔ LLM-generated responses grounded in the document
✔ Streamlit web UI + FastAPI backend

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
LLM (Ollama)
   └── Final Answer Generation
```

---

## Tech Stack

| Component   | Technology            |
| ----------- | --------------------- |
| Frontend UI | Streamlit             |
| REST API    | FastAPI               |
| Vector DB   | FAISS                 |
| Embeddings  | Sentence Transformers |
| LLM         | Ollama                |
| Language    | Python                |

---

## RAG Pipeline

1️⃣ User uploads a PDF
2️⃣ Extract full document text
3️⃣ Split text into overlapping chunks
4️⃣ Convert chunks into vector embeddings
5️⃣ Store them in a FAISS index
6️⃣ On query → Retrieve relevant chunks
7️⃣ Send them to the model to generate a grounded answer

---

## Project Structure

```
pdf_chatbot/
│
├── backend/
│   ├── routes/
│   │   └── ask_route.py
│   ├── services/
│   │   ├── extract_text.py
│   │   ├── chunk_text.py
│   │   ├── embeddings.py
│   │   ├── faiss_store.py
│   │   └── faiss_query.py
│   └── data/
│       ├── uploads/
│       ├── chunks/
│       └── faiss_indexes/
│
├── frontend/
│   └── app.py
│
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

---

## How to Run Locally

### 1️⃣ Create Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start Backend (FastAPI)

```bash
uvicorn main:app --reload --port 8000
```

### 4️⃣ Start Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

---

## API Overview

| Endpoint      | Method | Purpose                                     |
| ------------- | ------ | ------------------------------------------- |
| `/upload-doc` | POST   | Upload & process PDF Documents              |
| `/ask`        | POST   | Ask a question related to uploaded document |

---

## Author

Muhammad Ali Nawaz Malik
AI / Machine Learning Developer — Islamabad, Pakistan


