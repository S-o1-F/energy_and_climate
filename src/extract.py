import pymupdf
from config import DATA_DIR, OUTPUT_DIR
import json
from pathlib import Path

def extract_pdf(file_path: str):
    pages = []
    with pymupdf.open(file_path) as document:
        for page_number, page in enumerate(document):
            text = page.get_text("text", sort=True).strip()

            if not text:
                continue

            pages.append({
                "text": text,
                "page": page_number + 1,
                "source": Path(file_path).name
            })

    return pages

def save_extracted_text(pages, output_path):

    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True,exist_ok=True)

    with open(output_path,"w",encoding="utf-8") as file:
        json.dump(pages,file,ensure_ascii=False,indent=2)



if __name__ == "__main__":
    pages = extract_pdf(DATA_DIR / "guidlines" / "Dataflow1-GHG_clean.pdf")
    save_extracted_text(pages, OUTPUT_DIR / "extracted" / "Dataflow1-GHG.json")

    print(f"Extracted {len(pages)} pages.")
