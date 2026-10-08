from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from docling.chunking import HybridChunker


def load_and_chunk(filepath: str):

    # Docling does the parsing and returns .md file when loading, no need of separate parsing function
    loader= DoclingLoader(
        file_path=filepath,
        export_type=ExportType.DOC_CHUNKS,
        chunker=HybridChunker(tokenizer="sentence-transformers/all-MiniLM-L6-v2")
    )

    chunks = loader.load()
    print(f"[chunk] Created {len(chunks)} layout-aware chunks")
    return chunks
