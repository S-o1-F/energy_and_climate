import pymupdf
from src.config import DATA_DIR, OUTPUT_DIR
import json
from pathlib import Path
from docx import Document

def extract_pdf(file_path: str):
    pages = []
    with pymupdf.open(file_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text", sort=True).strip()

            if not text:
                continue

            pages.append({
                "text": text,
                "page": page_number,
                "source": Path(file_path).name
            })

    return pages

def extract_docx(file_path: str):
    document=Document(file_path)
    text="\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())

    if not text.strip():
        return []

    return [{
        "text": text,
        "page": None,
        "source": Path(file_path).name
    }]

def save_extracted_text(pages, output_path):
    with open(output_path,"w",encoding="utf-8") as file:
        json.dump(pages,file,ensure_ascii=False,indent=2)



if __name__ == "__main__":
    pages = extract_pdf(DATA_DIR / "romania" / "First_NECP_Romania.pdf")
    save_extracted_text(pages, OUTPUT_DIR / "extracted" / "First_NECP_Romania.json")

    print(f"Extracted {len(pages)} pages.")
