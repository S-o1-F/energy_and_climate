import json
from sentence_transformers import SentenceTransformer
from src.config import OUTPUT_DIR, EMBED_MODEL

_model=None

def create_embeddings(chunks):
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)

    texts=[chunk['text'] for chunk in chunks]
    embeddings=_model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    embedded_chunks=[]
    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append({
            **chunk,
            "embedding": embedding.tolist()
        })

    return embedded_chunks

