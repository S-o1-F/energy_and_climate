import json
from src.config import OUTPUT_DIR
from src.embeddings import create_embeddings
from src.index import insert_chunks

with open(OUTPUT_DIR / "charts" / "First_NECP_Romania_chart_chunks.json", encoding="utf-8") as f:
    chunks=json.load(f)
for chunk in chunks:
    chunk["id"]="chart_"+chunk["id"]
insert_chunks(create_embeddings(chunks))