# FOR CONTAINERIZATION - DOCKER

import os
import streamlit as st
import requests

# -----------------------------
# Configuration
# -----------------------------
# Backend API URL (use environment variable in Docker, fallback for local dev)
API_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

# Streamlit page configuration
st.set_page_config(page_title="PDF Chatbot", layout="centered")
st.title("📄 PDF Chatbot")

# -----------------------------
# Session state initialization
# -----------------------------
if 'doc_id' not in st.session_state:
    st.session_state['doc_id'] = None
if 'questions' not in st.session_state:
    st.session_state['questions'] = []
if 'answers' not in st.session_state:
    st.session_state['answers'] = []

# -----------------------------
# PDF Upload Section
# -----------------------------
st.subheader("Upload a Document")
uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

if uploaded_file:
    if st.button("Upload PDF"):
        try:
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(f"{API_URL}/upload-doc", files=files)
            if response.status_code == 200:
                data = response.json()
                st.session_state['doc_id'] = data['doc_id']
                st.success(f"PDF uploaded successfully! doc_id: {data['doc_id']}")
            else:
                st.error(f"Upload failed: {response.text}")
        except Exception as e:
            st.error(f"Upload error: {e}")

# -----------------------------
# Question / Answer Section
# -----------------------------
st.subheader("Ask a Question")
query_input = st.text_input("Enter your question:")

if st.button("Send Question"):
    if not st.session_state['doc_id']:
        st.warning("Please upload a PDF first.")
    elif not query_input.strip():
        st.warning("Please type a question.")
    else:
        try:
            payload = {"doc_id": st.session_state['doc_id'], "query": query_input}
            response = requests.post(f"{API_URL}/ask", json=payload)
            if response.status_code == 200:
                data = response.json()
                # Append to chat history
                st.session_state['questions'].append(query_input)
                st.session_state['answers'].append(data['answer'])
            else:
                st.error(f"Backend error: {response.text}")
        except Exception as e:
            st.error(f"Request error: {e}")

# -----------------------------
# Display Chat History
# -----------------------------
if st.session_state['questions']:
    st.subheader("Chat History")
    for q, a in zip(st.session_state['questions'], st.session_state['answers']):
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Bot:** {a}")
        st.markdown("---")

