import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer, CrossEncoder
from src.config import DB_URL, EMBED_MODEL, QUERY_PREFIX
import sys

RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_model = None
_reranker=None

def embed_query(question: str):
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model.encode(QUERY_PREFIX + question, normalize_embeddings=True)

def rerank(question, rows):
    global _reranker
    if _reranker is None:
        _reranker=CrossEncoder(RERANK_MODEL)
    scores=_reranker.predict([(question, row[3]) for row in rows])
    ranked=sorted(zip(scores, rows), key=lambda x: x[0], reverse=True)
    return [row for score, row in ranked]

def search(question: str, country: str | None = None, k: int = 5):
    query_vec = embed_query(question)
    with psycopg.connect(DB_URL) as conn:
        register_vector(conn)
        rows=  conn.execute(
            """
            SELECT source, page, section, content, 1 - (embedding <=> %(q)s) AS similarity
            FROM chunks
            WHERE %(country)s::text IS NULL OR country = %(country)s
            ORDER BY embedding <=> %(q)s
            LIMIT %(n)s
            """,
            {"q": query_vec, "country": country, "n": 50},
        ).fetchall()

    rows=rerank(question, rows)
    results=[]
    counts={}
    for row in rows:
        key=(row[1], row[2])
        counts[key]=counts.get(key,0)+1
        if counts[key]<=2:
            results.append(row)
        if len(results)==k:
            break
    return results

if __name__ == "__main__":
    #for source, page, section, content, sim in search("Current and projected progress towards other national greenhouse-gas related targets and objectives, including sector targets", country="RO"):
        #print(f"similarity: {sim:.3f} | {source} p.{page} | {content[:100]}")

    for source, page, section, content, sim in search(sys.argv[1], country="RS"):
        print(f"similarity: {sim:.3f} | p.{page} | {content[-120:]}")
