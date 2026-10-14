# rag.py
import os
import faiss
import requests
import pickle
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


def build_embeddings_from_model(chunks, model):
    """Embed chunks using a pre-loaded model."""
    texts = []
    for chunk in chunks:
        source = chunk.metadata.get("source", "")
        doc_title = Path(source).stem  
        texts.append(f"{doc_title}\n{chunk.page_content}")
    
    embeddings = model.encode(texts, show_progress_bar=True,normalize_embeddings=True)
    print(f"[embed] Shape: {embeddings.shape}")
    return embeddings


def build_index(embeddings):
    """Store embeddings in a FAISS index for fast search."""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype("float32"))
    print(f"[index] Stored {index.ntotal} vectors")
    return index


def save_pipeline(index, chunks):
    """Save FAISS index and chunks to disk."""
    faiss.write_index(index, str(INDEX_DIR / "index.faiss"))
    with open(INDEX_DIR / "chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    print("[Save] Saved index and chunks to disk.")


def load_pipeline():
    """Load FAISS index and chunks from disk if they exist."""
    index_path = INDEX_DIR / "index.faiss"
    chunks_path = INDEX_DIR / "chunks.pkl"
    
    if index_path.exists() and chunks_path.exists():
        index = faiss.read_index(str(index_path))
        with open(chunks_path, "rb") as f:
            chunks = pickle.load(f)
        print(f"[Save] Loaded {len(chunks)} chunks from disk.")
        return index, chunks
    
    print("[Save] No saved pipeline found. Starting fresh.")
    return None, []


def retrieve(question, embed_model, index, chunks, k=3):
    """Find the k most relevant chunks for a question."""
    q_vector = embed_model.encode([question],normalize_embeddings=True).astype("float32")
    distances, indices_found = index.search(q_vector, k=k)

    results = []
    for rank, idx in enumerate(indices_found[0]):
        dist = distances[0][rank]
        text = chunks[idx].page_content
        metadata = chunks[idx].metadata

        if dist < 0.8:
            confidence = "HIGH"
        elif dist < 1.2:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        results.append({"text": text, "distance": dist, "confidence": confidence, "metadata": metadata})

    filtered = [r for r in results if r["confidence"] != "LOW"]

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

