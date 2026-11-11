import json
from src.config import *
from src.index import insert_chunks
from src.extract import extract_docx, extract_pdf
from src.clean import clean_pages
from src.chunking import chunk_pages
from src.embeddings import create_embeddings
from src.tables.extract_tables import extract_tables
from src.tables.clean_tables import clean_tables
from src.tables.chunk_tables import table_to_chunks

def save_json(data,path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def process_tables(file_path, country, output_name):
    tables=clean_tables(extract_tables(file_path))
    table_chunks=table_to_chunks(tables, country)

    if table_chunks:
        insert_chunks(create_embeddings(table_chunks))

    save_json(tables, OUTPUT_DIR / "tables" / "cleaned" / output_name)
    save_json(table_chunks, OUTPUT_DIR / "tables" / "chunks" / output_name)

    print(f"Extracted {len(tables)} tables")
    print(f"Created {len(table_chunks)} table chunks")

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
    insert_chunks(embedded_chunks)

    output_name=f"{file_path.stem}.json"
    save_json(pages, OUTPUT_DIR / "extracted" / output_name)
    save_json(cleaned_pages, OUTPUT_DIR / "cleaned" / output_name)
    save_json(chunks, OUTPUT_DIR / "chunks" / output_name)
    #save_json(embedded_chunks, OUTPUT_DIR / "embeddings" / output_name)

    if ".pdf" in str(file_path).lower():
        process_tables(file_path, country, output_name)

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
    #run_pipeline()
    file_path = DATA_DIR / "romania" / "First_NECP_Romania.pdf"
    process_document(file_path, "RO")