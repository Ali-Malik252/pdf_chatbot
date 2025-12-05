import faiss
import numpy as np
from pathlib import Path

FAISS_DIR = Path(__file__).resolve().parent.parent / "data" / "faiss_indexes"
FAISS_DIR.mkdir(parents=True, exist_ok=True)

def create_faiss_index(doc_id: str, embeddings_file: Path):
    """
    Load embeddings and create FAISS index, then save to disk.
    
    Args:
        doc_id (str): Unique document ID
        embeddings_file (Path): Path to .npy embeddings file
    """
    # Load embeddings
    embeddings = np.load(embeddings_file).astype('float32')  # FAISS requires float32

    # Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index
    faiss_file = FAISS_DIR / f"{doc_id}_index.faiss"
    faiss.write_index(index, str(faiss_file))

    return faiss_file
