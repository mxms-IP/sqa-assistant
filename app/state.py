# state.py
from pathlib import Path

pipeline = {}

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"

INDEX_DIR = BASE_DIR / "data" / "index"
INDEX_DIR.mkdir(parents=True, exist_ok=True)

CHROMA_DIR = BASE_DIR / "data" / "chroma"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

HF_CACHE = BASE_DIR / "data" / "hf_cache"
HF_CACHE.mkdir(parents=True, exist_ok=True)