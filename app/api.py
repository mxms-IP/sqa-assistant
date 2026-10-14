# api.py
import sys
import os
from typing import List
import app.rag as rag  
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.models import AskResponse, AskRequest
from app.state import pipeline, UPLOAD_DIR, BASE_DIR

router= APIRouter()

@router.post("/api/ask", response_model=AskResponse)
def ask(request: AskRequest):
    retrieved = rag.retrieve(request.question, pipeline["embed_model"], pipeline["collection"])
    if not retrieved:
        return AskResponse(answer="Insufficient context, the documents do not contain enough relevant information to answer this question.", metadata=[])
    
    prompt = rag.build_prompt(request.question, retrieved)
    answer = rag.ask_llm(prompt)
    sources = [
        {
            "source": os.path.basename(r["metadata"]["source"]),
            "page": r['metadata']['page_no']
        }
        for r in retrieved
    ]

    return AskResponse(answer=answer,metadata=sources)

@router.post("/api/upload")
async def upload(files: List[UploadFile] = File(...)):

    chunks_list = list(pipeline.get("chunks", []))
    # 1. Only accept PDFs
    for file in files:
        if not file.filename.endswith((".pdf")):
            raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    
        # 2. Save the file to data/uploads/
        save_path = UPLOAD_DIR / file.filename
        contents = await file.read()
        with open(save_path, "wb") as f:
            f.write(contents)
        print(f"[upload] Saved {file.filename}")
        
        chunks = rag.load_and_chunk(str(save_path))

        rag.add_chunks_to_chroma(chunks, pipeline["embed_model"], pipeline["collection"])
        
    

    return {"message": "Files successfully uploaded", "filenames": [f.filename for f in files] , "chunks": len(chunks_list)}
