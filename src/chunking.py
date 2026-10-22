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
