"""
retrieval.py
------------
Hybrid retrieval for UCLA Dining RAG project.

Combines:
    - Dense search  : ChromaDB + all-MiniLM-L6-v2 cosine similarity
    - Sparse search : BM25 via rank_bm25 (BM25Okapi)

Results are fused with Reciprocal Rank Fusion (RRF) and the top-k
chunks are returned with their metadata.

Usage (standalone test):
    python retrieval.py
"""

from __future__ import annotations

import json
import pickle
import re
from pathlib import Path
from typing import Any

import chromadb
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CHUNKS_PATH    = "data/chunks.json"
CHROMA_DIR     = "data/chroma_db"
COLLECTION_NAME = "ucla_dining"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BM25_INDEX_PATH = "data/bm25_index.pkl"

TOP_K          = 5        # final results returned to caller
CANDIDATE_K    = 20       # candidates pulled from each retriever before fusion
RRF_K          = 60       # RRF smoothing constant (standard default)


# ---------------------------------------------------------------------------
# Tokeniser (shared by BM25 index + query)
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> list[str]:
    """Lowercase, remove punctuation, split on whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text.split()


# ---------------------------------------------------------------------------
# BM25 index — build or load
# ---------------------------------------------------------------------------

def build_bm25_index(chunks: list[dict], save_path: str = BM25_INDEX_PATH) -> BM25Okapi:
    """
    Tokenise all chunk texts and build a BM25Okapi index.
    Persists the index + chunk list to disk so it can be reloaded without
    re-running the full ingestion pipeline.
    
    The index is the data structure BM25 uses to efficiently score every chunk against a query without having to loop through raw text each time.
    Precomputes term freqs and doc statistics.
    """
    print("Building BM25 index…")
    corpus = [_tokenize(c["text"]) for c in chunks]
    index = BM25Okapi(corpus)

    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "wb") as fh:
        pickle.dump({"index": index, "chunks": chunks}, fh)

    print(f"✓ BM25 index saved to {save_path}  ({len(chunks)} docs)")
    return index


def load_bm25_index(
    save_path: str = BM25_INDEX_PATH,
    chunks_path: str = CHUNKS_PATH,
) -> tuple[BM25Okapi, list[dict]]:
    """
    Load a previously saved BM25 index.
    Falls back to rebuilding from chunks.json if the pickle doesn't exist.
    """
    p = Path(save_path)
    if p.exists():
        print(f"Loading BM25 index from {save_path}")
        with open(p, "rb") as fh:
            payload = pickle.load(fh)
        return payload["index"], payload["chunks"]

    # Fallback: rebuild
    print(f"BM25 index not found at {save_path} — rebuilding from {chunks_path}")
    with open(chunks_path, "r", encoding="utf-8") as fh:
        chunks = json.load(fh)
    index = build_bm25_index(chunks, save_path)
    return index, chunks


# ---------------------------------------------------------------------------
# Retriever class
# ---------------------------------------------------------------------------

class HybridRetriever:
    """
    Hybrid retriever combining BM25 sparse search and ChromaDB dense search
    via Reciprocal Rank Fusion (RRF).

    Parameters
    ----------
    top_k : int
        Number of final results to return.
    candidate_k : int
        Number of candidates to pull from each retriever before fusion.
    rrf_k : int
        RRF smoothing constant. Higher = less weight on top ranks.
    """

    def __init__(
        self,
        top_k: int = TOP_K,
        candidate_k: int = CANDIDATE_K,
        rrf_k: int = RRF_K,
        chroma_dir: str = CHROMA_DIR,
        collection_name: str = COLLECTION_NAME,
        model_name: str = EMBEDDING_MODEL,
        bm25_index_path: str = BM25_INDEX_PATH,
        chunks_path: str = CHUNKS_PATH,
    ):
        self.top_k = top_k
        self.candidate_k = candidate_k
        self.rrf_k = rrf_k

        # --- Dense retriever ---
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

        print(f"Connecting to ChromaDB at: {chroma_dir}")
        client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = client.get_collection(name=collection_name)

        # --- Sparse retriever ---
        self.bm25, self.chunks = load_bm25_index(bm25_index_path, chunks_path)

        # Lookup: chunk_id → chunk dict (for metadata after BM25 results)
        self._chunk_map: dict[str, dict] = {c["chunk_id"]: c for c in self.chunks}

        print("✓ HybridRetriever ready\n")

    # ------------------------------------------------------------------
    # Dense search
    # ------------------------------------------------------------------

    def _dense_search(self, query: str) -> list[dict]:
        """
        Query ChromaDB with an embedded query vector.
        Returns up to candidate_k results, each as:
            { chunk_id, text, score, metadata }
        where score is cosine distance (lower = more similar).
        """
        query_vec = self.model.encode(query, convert_to_list=True) # prompt must be encoded too for comparison
        results = self.collection.query( # query "table"
            query_embeddings=[query_vec],
            n_results=self.candidate_k,
            include=["documents", "metadatas", "distances"],
        )

        hits = []
        for doc_id, doc, meta, dist in zip(
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            hits.append( # ChromeDB returns exactly n_results regardless of their score
                {
                    "chunk_id": doc_id,
                    "text":     doc,
                    "score":    dist,     # cosine distance; lower = better
                    "metadata": meta,
                }
            )
        return hits  # already ordered best → worst by ChromaDB

    # ------------------------------------------------------------------
    # Sparse search
    # ------------------------------------------------------------------

    def _sparse_search(self, query: str) -> list[dict]:
        """
        Query the BM25 index with a tokenised query.
        Returns up to candidate_k results, each as:
            { chunk_id, text, score, metadata }
        where score is the BM25 score (higher = more relevant).
        """
        tokens = _tokenize(query)
        scores = self.bm25.get_scores(tokens) # doc statistics and freqs

        # Pair each chunk with its BM25 score and sort descending
        scored = sorted(
            enumerate(scores), key=lambda x: x[1], reverse=True
        )[: self.candidate_k]

        hits = []
        for idx, score in scored:
            chunk = self.chunks[idx]
            hits.append(
                {
                    "chunk_id": chunk["chunk_id"],
                    "text":     chunk["text"],
                    "score":    score,
                    "metadata": {
                        "source_id":   chunk["source_id"],
                        "source_name": chunk["source_name"],
                        "source_type": chunk["source_type"],
                        "description": chunk["description"],
                        "url":         chunk["url"],
                        "chunk_index": chunk["chunk_index"],
                    },
                }
            )
        return hits

    # ------------------------------------------------------------------
    # Reciprocal Rank Fusion
    # ------------------------------------------------------------------

    def _rrf_fusion(
        self,
        dense_hits: list[dict],
        sparse_hits: list[dict],
    ) -> list[dict]:
        """
        Merge two ranked lists (without caring about the actual scores) using Reciprocal Rank Fusion.

        RRF score for a document d:
            RRF(d) = Σ  1 / (k + rank_i(d))
        where i is each retriever, rank_i(d) is the 1-based position of d in retriever i's list.
        k is smoothing constant so top rank doesn't dominate too heavily (so 1 isn't infinitely better than 2)
        Retrievers here mean BM25 rank and cosine distance rank, so two sums for each chunk.

        Higher RRF score = more relevant.
        """
        rrf_scores: dict[str, float] = {}

        for rank, hit in enumerate(dense_hits, start=1): # computing the sums independently
            cid = hit["chunk_id"]
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + 1.0 / (self.rrf_k + rank)

        for rank, hit in enumerate(sparse_hits, start=1):
            cid = hit["chunk_id"]
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + 1.0 / (self.rrf_k + rank)

        # Build a unified result list
        all_hits: dict[str, dict] = {}
        for hit in dense_hits + sparse_hits:
            cid = hit["chunk_id"]
            if cid not in all_hits:
                all_hits[cid] = hit

        fused = sorted( # take all the hits and then sort them by RRF ranking
            all_hits.values(),
            key=lambda h: rrf_scores[h["chunk_id"]],
            reverse=True,
        )

        # Attach the fused RRF score for transparency
        for hit in fused:
            hit["rrf_score"] = rrf_scores[hit["chunk_id"]]

        return fused[: self.top_k]

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def retrieve(self, query: str) -> list[dict]:
        """
        Run hybrid retrieval for a query string.

        Returns top_k chunk dicts, each containing:
            chunk_id, text, metadata, rrf_score
        """
        dense_hits  = self._dense_search(query)
        sparse_hits = self._sparse_search(query)
        return self._rrf_fusion(dense_hits, sparse_hits)

    def retrieve_and_print(self, query: str) -> list[dict]:
        """Retrieve and pretty-print results. Useful for interactive testing."""
        results = self.retrieve(query)
        print(f"\nQuery: {query!r}")
        print(f"Top {len(results)} results (hybrid BM25 + ChromaDB):\n")
        for i, hit in enumerate(results, start=1):
            m = hit["metadata"]
            print(
                f"  [{i}] {m['source_name']} — {m['description']}"
                f"  (rrf={hit['rrf_score']:.4f})"
            )
            print(f"       url:  {m['url']}")
            print(f"       text: {hit['text']}\n")
        return results
    
    
    # ---------------------------------------------------------------------------
    # Hybrid Search Comparison
    # ---------------------------------------------------------------------------

    def compare_search_methods(self, query: str) -> dict:
        """
        Run BM25, dense, and hybrid search separately and return all three
        result sets for comparison.
        """
        dense_hits  = self._dense_search(query)[:5]
        sparse_hits = self._sparse_search(query)[:5]
        hybrid_hits = self.retrieve(query)

        return {
            "query":   query,
            "dense":   dense_hits,
            "sparse":  sparse_hits,
            "hybrid":  hybrid_hits,
        }

    def print_comparison(self, query: str) -> None:
        results = self.compare_search_methods(query)

        print(f"\n{'='*60}")
        print(f"Query: {query!r}")
        print(f"{'='*60}")

        for method in ["dense", "sparse", "hybrid"]:
            print(f"\n--- {method.upper()} ---")
            for i, hit in enumerate(results[method], start=1):
                m = hit["metadata"]
                score = hit.get("rrf_score", hit.get("score", "n/a"))
                print(f"  [{i}] {m['source_name']} — {m['description']}")
                print(f"       score: {score:.4f}")
                print(f"       text:  {hit['text'][:100]}…")


# ---------------------------------------------------------------------------
# Entry point — quick smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    retriever = HybridRetriever()

    test_queries = [
        "Which dining hall hosted the Harry Potter dinner?",
        "What are good options for students with dietary restrictions?",
        "How do meal plans work for commuters?",
    ]

    for q in test_queries:
        retriever.print_comparison(q)
        print("─" * 60)
