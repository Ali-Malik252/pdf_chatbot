import pdfplumber
from typing import List
from pathlib import Path

# Base directory: backend/
BASE_DIR = Path(__file__).resolve().parent.parent

# Directory to save uploaded PDFs
UPLOAD_FOLDER = BASE_DIR / "data" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

def extract_text_from_pdf(file_path: str) -> List[str]:
    """
    Extracts text from a PDF file page by page.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        List[str]: List where each element is the text of a page.
    """
    pages_text = []

    # Open the PDF using pdfplumber
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                pages_text.append(text.strip())  # Remove leading/trailing whitespace
            else:
                pages_text.append("")  # Empty string if page has no text

    return pages_text
