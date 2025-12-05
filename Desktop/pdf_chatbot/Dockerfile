# Backend Dockerfile

# Base Image
# Use lightweight Python 3.11
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy only what's needed for backend first to take advantage of layer caching
COPY backend/requirements.txt /app/backend/requirements.txt
# Install backend python deps
RUN pip install --upgrade pip
RUN pip install -r /app/backend/requirements.txt

# Copy entire project into container (main.py and backend, frontend kept for reference)
COPY . /app

# Ensure directories exist for runtime
RUN mkdir -p /app/backend/data/uploads /app/backend/data/chunks /app/backend/data/faiss_indexes

# Expose FastAPI port
EXPOSE 8000

# Default command to run FastAPI
# Run main.py as FastAPI entry point
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
