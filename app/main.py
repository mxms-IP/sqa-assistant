

import os
import sys
from pathlib import Path
import threading
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse 

import app.rag as rag
from app.api import router as api_router 
from app.state import pipeline, UPLOAD_DIR, BASE_DIR, CHROMA_DIR

sys.path.append(os.path.dirname(__file__))
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads" 


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    threading.Thread(target=load_assistant, daemon=True).start()
    
    yield

app= FastAPI(lifespan= lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

def load_assistant():
    print("[startup] Loading embedding model...")
    pipeline["embed_model"] = rag.load_embed_model()

    pipeline["collection"] = rag.get_chroma_collection(str(CHROMA_DIR))

    print("[startup] Ready.")
    pipeline["ready"] = True

@app.get("/home")
def home():
    return FileResponse(str(BASE_DIR / "public" /"index.html"))

@app.get("/health")
def health():
    if pipeline.get("ready"):
        return {"status": "ok"}
    else:
        return {"status": "loading"}

