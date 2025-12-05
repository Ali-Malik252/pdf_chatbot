from sentence_transformers import SentenceTransformer
import numpy as np

# Load once globally (CPU-friendly all-MiniLM-L6-v2)
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(texts):
    """
    Generate embeddings for a list of texts using Sentence Transformers.

    Args:
        texts (List[str]): List of text chunks

    Returns:
        np.ndarray: Embedding vectors
    """
    embeddings = model.encode(texts, convert_to_numpy=True, batch_size=16, normalize_embeddings=True)
    return embeddings
