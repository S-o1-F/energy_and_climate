import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer
from src.config import DB_URL, EMBED_MODEL, QUERY_PREFIX

_model = None

def embed_query(question: str):
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model.encode(QUERY_PREFIX + question, normalize_embeddings=True)

def search(question: str, country: str | None = None, k: int = 5):
    query_vec = embed_query(question)
    with psycopg.connect(DB_URL) as conn:
        register_vector(conn)
        return conn.execute(
            """
            SELECT source, page, section, content, 1 - (embedding <=> %(q)s) AS similarity
            FROM chunks
            WHERE %(country)s::text IS NULL OR country = %(country)s
            ORDER BY embedding <=> %(q)s
            LIMIT %(k)s
            """,
            {"q": query_vec, "country": country, "k": k},
        ).fetchall()

if __name__ == "__main__":
    for source, page, section, content, sim in search("Current and projected progress towards other national greenhouse-gas related targets and objectives, including sector targets", country="RO"):
        print(f"similarity: {sim:.3f} | {source} p.{page} | {content[:100]}")