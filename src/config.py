from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
DB_URL = "postgresql://rag:rag@localhost:5432/rag_db"   # user:password@host:port/database
LLM_MODEL="qwen2.5:3b"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

CHUNK_WORDS = 200
OVERLAP_WORDS = 40
MIN_WORDS = 30

COUNTRY = {"romania": "RO", "serbia": "RS", "guidlines": "EU"}

DOC_SETTINGS={
    "First_NECP_Romania.pdf":{
        "skip_2_col": True,
        "running_header": "The 2021-2030 Integrated National Energy and Climate Plan",
    },
}

DEFAULT_SETTINGS={
"First_NECP_Romania.pdf":{
        "skip_2_col": False,
        "running_header": None,
    },
}