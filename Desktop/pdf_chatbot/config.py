# from pathlib import Path

# # Base directory of the project
# BASE_DIR = Path(__file__).resolve().parent

# # Data folders
# UPLOAD_FOLDER = BASE_DIR / "backend" / "data" / "uploads"
# CHUNK_FOLDER = BASE_DIR / "backend" / "data" / "chunks"
# FAISS_FOLDER = BASE_DIR / "backend" / "data" / "faiss_indexes"

# # Make sure all folders exist
# for folder in [UPLOAD_FOLDER, CHUNK_FOLDER, FAISS_FOLDER]:
#     folder.mkdir(parents=True, exist_ok=True)


# FOR CONTAINERIZATION - DOCKER

import os
from pathlib import Path

# Base directory: backend root directory
BASE_DIR = Path(__file__).resolve().parent

# Data folder inside backend container
DATA_DIR = BASE_DIR / "backend" / "data"

# Sub-folders for files, chunks, embeddings
UPLOAD_FOLDER = DATA_DIR / "uploads"
CHUNK_FOLDER = DATA_DIR / "chunks"
FAISS_FOLDER = DATA_DIR / "faiss_indexes"

# Ensure directories exist (Docker volume mounted here)
for folder in [UPLOAD_FOLDER, CHUNK_FOLDER, FAISS_FOLDER]:
    os.makedirs(folder, exist_ok=True)
