import json
from src.config import *
from src.extract import extract_docx, extract_pdf
from src.clean import clean_pages
from src.chunking import chunk_pages
from src.embeddings import create_embeddings

def save_json(data,path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

def process_document(file_path, country):
    print("Processing file: ", file_path.name)

    if ".pdf" in str(file_path).lower():
        pages=extract_pdf(str(file_path))
    elif "docx" in str(file_path).lower():
        pages=extract_docx(str(file_path))
    else:
        return

    if not pages:
        print("There are no pages found.")
        return

    cleaned_pages=clean_pages(pages)
    chunks=chunk_pages(cleaned_pages, country=country)
    embedded_chunks=create_embeddings(chunks)

    output_name=f"{file_path.stem}.json"
    save_json(pages, OUTPUT_DIR / "extracted" / output_name)
    save_json(cleaned_pages, OUTPUT_DIR / "cleaned" / output_name)
    save_json(chunks, OUTPUT_DIR / "chunks" / output_name)
    save_json(embedded_chunks, OUTPUT_DIR / "embeddings" / output_name)

    print(f"Pages extracted: {len(pages)}")
    print(f"Created {len(chunks)} chunks")
    print(f"Created {len(embedded_chunks)} embeddings")


def run_pipeline():
    for folder_name, country in COUNTRY.items():
        folder=DATA_DIR / folder_name
        files=sorted(file_path for file_path in folder.rglob("*") if file_path.is_file() and file_path.suffix.lower() in [".docx", ".pdf"])
        print(f"\n{folder_name}, {country}, {len(files)} files")

        for file_path in files:
            process_document(file_path, country)

if __name__ == "__main__":
    run_pipeline()