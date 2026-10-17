# rag.py
import os
import requests
import pickle
import chromadb
import numpy as np
from google import genai
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from docling.chunking import HybridChunker
from app.state import HF_CACHE,INDEX_DIR


load_dotenv()
os.environ["HF_HOME"] = str(HF_CACHE)



# Load and parse using docling (layout-aware) 
def load_and_chunk(filepath: str):
    """
    Load and parse the file using docling (layout-aware). 
    Docling does the parsing and returns .md file when loading.
    Then, docling's native HybridChunker creates chunks.
    """
    loader= DoclingLoader(
        file_path=filepath,
        export_type=ExportType.DOC_CHUNKS,
        chunker=HybridChunker(tokenizer="BAAI/bge-small-en-v1.5")
    )

    chunks = loader.load()
    print(f"[chunk] Created {len(chunks)} layout-aware chunks")
    return chunks


def load_embed_model():
    """Load the embedding model. Call this once and reuse."""
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    print("[embed] Model loaded.")
    return model

def add_chunks_to_chroma(chunks, embed_model, collection):
    texts = []
    ids = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get("source", "")
        doc_title = Path(source).stem
        text = f"{doc_title}\n{chunk.page_content}"
        texts.append(text)
        ids.append(f"{doc_title}_chunk_{i}")

        #because docling does not provide flatten metadata
        raw = chunk.metadata
        dl_meta = raw.get("dl_meta", {})
        doc_items = dl_meta.get("doc_items", [{}])
        first_prov = doc_items[0].get("prov", [{}])[0] if doc_items else {}

        metadatas.append({
            "source": raw.get("source", ""),
            "page_no": first_prov.get("page_no", -1),
            "doc_title": doc_title
        })

    embeddings = embed_model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    ).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"[chroma] Added {len(texts)} chunks to collection")


def get_chroma_collection(chroma_dir: str):
    client = chromadb.PersistentClient(path=chroma_dir)
    collection = client.get_or_create_collection(
        name="sqa_documents",
        metadata={"hnsw:space": "cosine"}
    )
    return collection

def retrieve(question, embed_model, collection, k=3):
    q_vector = embed_model.encode(
        [question],
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=q_vector,
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    formatted = []
    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]
        
        if distance < 0.2:
            confidence = "HIGH"
        elif distance < 0.5:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        formatted.append({
            "text": results["documents"][0][i],
            "distance": distance,
            "confidence": confidence,
            "metadata": results["metadatas"][0][i]
        })

    filtered = [r for r in formatted if r["confidence"] != "LOW"]
    return filtered if filtered else []


def build_prompt(question, retrieved):
    """Assemble the context + question into a prompt string."""
    context = "\n\n".join([r["text"] for r in retrieved])
    prompt = f"""You are a helpful assistant. You must follow these rules strictly:
RULE 1: Use ONLY the context below to answer. Do not add outside knowledge.
RULE 2: If the context does not contain enough information, respond with exactly: "The document does not answer this question."
RULE 3: Keep your answer to 2-3 sentences maximum.

Context:
{context}

Question: {question}
Answer (2-3 sentences, context only):"""
    return prompt


def ask_llm(prompt, model_name="gemini-3.5-flash-lite"):
    client = genai.Client()
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    
    return response.text

