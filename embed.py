"""
embed.py
--------
Embedding pipeline for UCLA Dining RAG project.

Loads chunks from data/chunks.json, embeds them with all-MiniLM-L6-v2
via SentenceTransformers, and stores them in a persistent ChromaDB collection
with full source metadata.

Usage:
    python embed.py
"""

from __future__ import annotations

import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CHUNKS_PATH = "data/chunks.json"
CHROMA_DIR = "data/chroma_db"
COLLECTION_NAME = "ucla_dining"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 64          # embed this many chunks at a time
TOP_K_PREVIEW = 5        # how many entries to show in the preview method


# ---------------------------------------------------------------------------
# Load chunks
# ---------------------------------------------------------------------------

def load_chunks(path: str = CHUNKS_PATH) -> list[dict]:
    """Load chunk dicts produced by ingest_and_chunk.py."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"Chunks file not found at {path!r}. "
            "Run ingest_and_chunk.py first."
        )
    with open(p, "r", encoding="utf-8") as fh:
        chunks = json.load(fh)
    print(f"Loaded {len(chunks)} chunks from {path}")
    return chunks


# ---------------------------------------------------------------------------
# Embedding + ChromaDB storage
# ---------------------------------------------------------------------------

def build_vector_store(
    chunks: list[dict],
    chroma_dir: str = CHROMA_DIR,
    collection_name: str = COLLECTION_NAME,
    model_name: str = EMBEDDING_MODEL,
    batch_size: int = BATCH_SIZE,
) -> chromadb.Collection:
    """
    Embed all chunks and upsert into a persistent ChromaDB collection.

    Each chunk is stored with:
    - embedding  : 384-dim float vector (all-MiniLM-L6-v2)
    - document   : the chunk text
    - metadata   : source_id, source_name, source_type, description,
                    url, chunk_index
    - id         : chunk_id  (e.g. "2_0", "2_1", …)
    """
    print(f"\nLoading embedding model: {model_name}")
    model = SentenceTransformer(model_name)

    print(f"Connecting to ChromaDB at: {chroma_dir}")
    client = chromadb.PersistentClient(path=chroma_dir)

    # Get or create collection (cosine similarity matches MiniLM training)
    collection = client.get_or_create_collection( # equivalent of a table in a relational db
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    # Split into batches
    total = len(chunks)
    for batch_start in range(0, total, batch_size):
        batch = chunks[batch_start : batch_start + batch_size]

        texts = [c["text"] for c in batch]
        ids = [c["chunk_id"] for c in batch]
        metadatas = [
            {
                "source_id":   c["source_id"],
                "source_name": c["source_name"],
                "source_type": c["source_type"],
                "description": c["description"],
                "url":         c["url"],
                "chunk_index": c["chunk_index"],
            }
            for c in batch
        ]

        embeddings = model.encode(
            texts,
            show_progress_bar=False,
            convert_to_list=True,
        )

        collection.upsert( # insert into "table"
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        end = min(batch_start + batch_size, total)
        print(f"  Upserted chunks {batch_start + 1}–{end} / {total}")

    print(f"\n✓ Collection '{collection_name}' — {collection.count()} entries total")
    return collection


# ---------------------------------------------------------------------------
# Preview: top ChromaDB entries
# ---------------------------------------------------------------------------

def preview_top_entries(
    collection: chromadb.Collection,
    n: int = TOP_K_PREVIEW,
) -> None:
    """
    Print the first n entries stored in the ChromaDB collection.
    Useful for a quick sanity-check after embedding.
    """
    result = collection.peek(limit=n)
    print(f"\n--- Top {n} ChromaDB entries ---")
    for i, (doc_id, doc, meta) in enumerate(
        zip(result["ids"], result["documents"], result["metadatas"])
    ):
        print(
            f"\n[{i+1}] id={doc_id} | {meta['source_name']} — {meta['description']}"
        )
        print(f"     url:   {meta['url']}")
        print(f"     chars: {len(doc)}")
        print(f"     text:  {doc[:120]}…")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    chunks = load_chunks()
    collection = build_vector_store(chunks)
    preview_top_entries(collection)
