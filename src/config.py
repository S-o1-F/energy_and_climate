from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
DB_URL = "postgresql://rag:rag@localhost:5432/rag_db"   # user:password@host:port/database
LLM_MODEL="qwen2.5:7b"
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
    "RS_NECP.pdf": {
        "skip_2_col": False,
        "running_header": None,
    },
}

DEFAULT_SETTINGS={
"First_NECP_Romania.pdf":{
        "skip_2_col": False,
        "running_header": None,
    },
}

SKIP_TABLES = {
    "RS_NECP.pdf": ["p284_t0", "p285_t0", "p286_t0", "p287_t0", "p291_t0", "p292_t0", "p293_t0", "p294_t0", "p295_t0", "p295_t1", "p296_t0", "p297_t0", "p298_t0",
"p299_t0", "p299_t1", "p300_t0", "p300_t1", "p301_t0", "p302_t0", "p303_t0", "p303_t1", "p304_t0",],
}