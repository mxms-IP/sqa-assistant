# api.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from typing import List
import sys
import os
import app.rag as rag  
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from app.rag_pipe.chunking import load_and_chunk

sys.path.append(os.path.dirname(__file__))

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"  

# create pipeline dictionary to store model, chunks and embeddings
pipeline = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[startup] Loading embedding model...")
    pipeline["embed_model"] = rag.load_embed_model()
    
    index, chunks = rag.load_pipeline()
    if index is not None:
        pipeline["index"] = index
        pipeline["chunks"] = chunks
        print("[startup] Pipeline restored from disk.")
    
    print("[startup] Ready.")
    yield


app = FastAPI(lifespan=lifespan)\

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defining request body
class AskRequest(BaseModel):
    question: str
    

# Defining response body
class AskResponse(BaseModel):
    answer: str
    metadata: list

@app.get("/api/home")
def home():
    return FileResponse(str(BASE_DIR / "public" /"index.html"))

@app.post("/api/ask", response_model=AskResponse)
def ask(request: AskRequest):
    retrieved = rag.retrieve(request.question, pipeline["embed_model"], pipeline["index"], pipeline["chunks"])
    if not retrieved:
        return AskResponse(answer="Insufficient context, the documents do not contain enough relevant information to answer this question.", metadata=[])
    
    prompt = rag.build_prompt(request.question, retrieved)
    answer = rag.ask_llm(prompt)
    sources = [
        {
            "source": os.path.basename(r["metadata"]["source"]),
            "page": r['metadata']['dl_meta']['doc_items'][0]['prov'][0]['page_no']
        }
        for r in retrieved
    ]

    return AskResponse(answer=answer,metadata=sources)

@app.post("/api/upload")
async def upload(files: List[UploadFile] = File(...)):

    chunks_list = list(pipeline.get("chunks", []))
    # 1. Only accept PDFs
    for file in files:
        if not file.filename.endswith((".pdf", ".md")):
            raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    
        # 2. Save the file to data/uploads/
        save_path = UPLOAD_DIR / file.filename
        contents = await file.read()
        with open(save_path, "wb") as f:
            f.write(contents)
        print(f"[upload] Saved {file.filename}")
        
        chunks = load_and_chunk(str(save_path))
        chunks_list.extend(chunks)

    print("---------------------------------Chunks---------------------------------")
    for chunk in chunks_list:
        print(chunk)
        
    
    embeddings = rag.build_embeddings_from_model(chunks_list, pipeline["embed_model"])
    new_index = rag.build_index(embeddings)

    # 4. Replace the active index — now /ask searches the new document
    pipeline["index"] = new_index
    pipeline["chunks"] = chunks_list
    rag.save_pipeline(new_index, chunks_list)

    return {"message": "Files successfully uploaded", "filenames": [f.filename for f in files] , "chunks": len(chunks_list)}
