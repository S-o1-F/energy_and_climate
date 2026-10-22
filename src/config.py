from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
DB_PATH=OUTPUT_DIR / "chroma"

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

CHUNK_WORDS = 200
OVERLAP_WORDS = 40
MIN_WORDS = 30

COUNTRY = {"romania": "RO", "serbia": "RS", "guidlines": "EU"}