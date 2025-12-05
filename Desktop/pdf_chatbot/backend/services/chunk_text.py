from typing import List, Dict
from pathlib import Path

# Base directory: two levels up from this file (backend/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Directory to save chunk JSON files
CHUNK_FOLDER = BASE_DIR / "data" / "chunks"
CHUNK_FOLDER.mkdir(parents=True, exist_ok=True)

def create_text_chunks(
    doc_id: str,
    pages_text: List[str],
    chunk_size: int = 500,
    overlap: int = 100
) -> List[Dict]:
    """
    Splits extracted PDF text into smaller chunks with overlap.

    Args:
        doc_id (str): Unique document ID
        pages_text (List[str]): List of text per page
        chunk_size (int): Number of characters per chunk
        overlap (int): Number of characters to overlap between chunks

    Returns:
        List[Dict]: List of chunks with metadata
    """
    chunks = []
    chunk_id = 0

    for page_number, page_text in enumerate(pages_text, start=1):
        page_text = page_text.strip()  # remove leading/trailing spaces
        start = 0
        text_length = len(page_text)

        while start < text_length:
            end = min(start + chunk_size, text_length)  # don't go past end
            chunk_text = page_text[start:end]

            chunks.append({
                "doc_id": doc_id,
                "page_number": page_number,
                "chunk_id": chunk_id,
                "text": chunk_text
            })

            chunk_id += 1
            start += chunk_size - overlap  # move start forward with overlap

    return chunks
