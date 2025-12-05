import numpy as np
from pathlib import Path

# Path to your embeddings file
emb_file = Path(r"C:/Users/hp\Desktop/pdf_chatbot/backend/data/chunks/6f1f2228-b44e-4d78-a355-2f71c48556ff_embeddings.npy")
# Load embeddings
embeddings = np.load(emb_file)

print(f"Embeddings shape: {embeddings.shape}")
print("First embedding vector (first 10 values):")
print(embeddings[0][:10])
