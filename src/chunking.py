import json
from src.config import OUTPUT_DIR, COUNTRY

def chunk_pages(pages: list[dict], country: str,chunk_size: int=200, overlap:int=40, )->list[dict]:
    chunks=[]
    step=chunk_size-overlap

    for page in pages:
        words=page["text"].split()

        for j, start in enumerate(range(0, len(words), step)):
            piece=" ".join(words[start:start+chunk_size])
            if not piece:
                continue

            chunks.append({
                "id": f"{page['source']}_p{page['page']}_c{j}",
                "source": page['source'],
                "country": country,
                "page": page['page'],
                "text": piece,
            })

    return chunks

if __name__ == "__main__":
    input_path = OUTPUT_DIR / "cleaned" / "First_NECP_Romania.json"
    output_path = OUTPUT_DIR / "chunks" / "First_NECP_Romania.json"

    with open(input_path, "r", encoding="utf-8") as file:
        pages = json.load(file)

    country=COUNTRY['romania']

    chunks = chunk_pages(pages, country=country, chunk_size=200, overlap=40)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)

    print(f"Created {len(chunks)} chunks.")

