import psycopg
import numpy as np
from pgvector.psycopg import register_vector
from src.config import DB_URL

def insert_chunks(embedded_chunks: list[dict]):
    with psycopg.connect(DB_URL) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO chunks (id, country, page, source, section, content, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE
                SET content = EXCLUDED.content, embedding = EXCLUDED.embedding
                """,
                [
                    (c["id"], c["country"], c["page"], c["source"], c.get("section"),
                     c["text"], np.array(c["embedding"]))
                    for c in embedded_chunks
                ],
            )
    print(f"Inserted {len(embedded_chunks)} chunks")
