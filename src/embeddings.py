import json
from sentence_transformers import SentenceTransformer
from src.config import OUTPUT_DIR, EMBED_MODEL

_model=None

def create_embeddings(chunks):
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)

    texts=[chunk['text'] for chunk in chunks]
    embeddings=_model.encode(texts, show_progress_bar=True)

    embedded_chunks=[]
    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append({
            **chunk,
            "embedding": embedding.tolist()
        })

    return embedded_chunks

if __name__ == "__main__":
    input_path = OUTPUT_DIR / "chunks" / "First_NECP_Romania.json"
    output_path = OUTPUT_DIR / "embeddings" / "First_NECP_Romania.json"

    with open(input_path, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    embedded_chunks = create_embeddings(chunks)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(embedded_chunks, file, ensure_ascii=False)

    print(f"Created embeddings for {len(embedded_chunks)} chunks.")