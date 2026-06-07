"""
ingest_and_chunk.py
-------------------
Ingestion and chunking pipeline for UCLA Dining RAG project.

Supports two source types:
    - Reddit JSON  (fetched live via requests + Reddit JSON API, or loaded from a local .json file)
    - Plain-text   (.txt files, e.g. copy-pasted article content)

Chunking uses LangChain's RecursiveCharacterTextSplitter
    chunk_size  = 600 characters
    chunk_overlap = 100 characters

Output: list[dict] : each dict is one chunk with metadata attached.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any

import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100

# Fake a browser so Reddit doesn't return 429 / 403
REDDIT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; UCLADiningRAG/1.0; research project)"
}

# Seconds to wait between Reddit requests (be polite)
REDDIT_REQUEST_DELAY = 2.0

# ---------------------------------------------------------------------------
# Source registry
# (add / remove entries as needed; set local_path when you have a saved file)
# ---------------------------------------------------------------------------

SOURCES: list[dict] = [
    # --- Reddit sources ---
    {
        "id": 1,
        "source_type": "reddit",
        "source_name": "Reddit",
        "description": "UCLA Dining wiki",
        "url": "https://www.reddit.com/r/ucla/wiki/ucladining/",
        "local_path": "data/reddit_1.json",
    },
    {
        "id": 2,
        "source_type": "reddit",
        "source_name": "Reddit",
        "description": "How's the food at UCLA?",
        "url": "https://www.reddit.com/r/ucla/comments/123arn7/hows_the_food_at_ucla/",
        "local_path": "data/reddit_2.json",
    },
    {
        "id": 3,
        "source_type": "reddit",
        "source_name": "Reddit",
        "description": "Gluten intolerant dining",
        "url": "https://www.reddit.com/r/ucla/comments/15v0jh7/how_rough_is_dining_if_you_are_gluten_intolerant/",
        "local_path": "data/reddit_3.json",
    },
    {
        "id": 4,
        "source_type": "reddit",
        "source_name": "Reddit",
        "description": "Comprehensive dining hall ranking",
        "url": "https://www.reddit.com/r/ucla/comments/rvo8oo/comprehensive_dining_hall_ranking/",
        "local_path": "data/reddit_4.json",
    },
    {
        "id": 5,
        "source_type": "reddit",
        "source_name": "Reddit",
        "description": "Meals as a commuter",
        "url": "https://www.reddit.com/r/ucla/comments/1kl3qwz/meals_as_a_commuter/",
        "local_path": "data/reddit_5.json",
    },
    # --- Plain-text article sources ---
    {
        "id": 6,
        "source_type": "txt",
        "source_name": "BruinLife",
        "description": "Where to eat at UCLA - meal plans & dining halls",
        "url": "https://bruinlife.com/where-to-eat-at-ucla-meal-plans-dining-halls-and-campus-spots/",
        "local_path": "data/bruinlife_6.txt",
    },
    {
        "id": 7,
        "source_type": "txt",
        "source_name": "BruinLife",
        "description": "Top 5 best and worst foods at UCLA dining halls",
        "url": "https://bruinlife.com/top-5-best-and-worst-foods-at-the-ucla-dining-halls/",
        "local_path": "data/bruinlife_7.txt",
    },
    {
        "id": 8,
        "source_type": "txt",
        "source_name": "DailyBruin",
        "description": "Schedule changes to strikes - student dining experiences",
        "url": "https://dailybruin.com/2025/06/08/from-schedule-changes-to-strikes-students-discuss-ucla-dining-experiences",
        "local_path": "data/dailybruin_8.txt",
    },
    {
        "id": 9,
        "source_type": "txt",
        "source_name": "DailyBruin",
        "description": "Opinion: dietary restrictions deserve accurate info",
        "url": "https://dailybruin.com/2026/01/20/opinion-students-with-dietary-restrictions-deserve-accurate-information-from-ucla-dining",
        "local_path": "data/dailybruin_9.txt",
    },
    {
        "id": 10,
        "source_type": "txt",
        "source_name": "SpoonUniversity",
        "description": "Why themed dinners made UCLA dining halls great",
        "url": "https://spoonuniversity.com/school/ucla/why-themed-dinners-made-ucla-s-dining-halls/",
        "local_path": "data/spoon_10.txt",
    },
]


# ---------------------------------------------------------------------------
# Cleaning helpers
# ---------------------------------------------------------------------------

def _clean_text(text: str) -> str:
    """Remove excessive whitespace, boilerplate Reddit markdown artefacts, etc."""
    # Collapse multiple blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip leading/trailing whitespace on every line
    text = "\n".join(line.strip() for line in text.splitlines())
    # Remove Reddit vote/score artefacts like "↑ 42 points"
    text = re.sub(r"[↑↓]\s*\d+\s*(points?)?", "", text)
    # Remove markdown link syntax, keep visible text:  [text](url) → text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Remove leftover bare URLs
    text = re.sub(r"https?://\S+", "", text)
    # Remove repeated punctuation artefacts like "---" or "***"
    text = re.sub(r"[-*_]{3,}", "", text)
    # Final strip
    return text.strip()


# ---------------------------------------------------------------------------
# Reddit ingestion
# ---------------------------------------------------------------------------

def _reddit_json_url(url: str) -> str:
    """Convert a standard Reddit URL to its .json equivalent."""
    url = url.rstrip("/")
    if not url.endswith(".json"):
        url += ".json"
    return url


def _extract_reddit_wiki(data: Any) -> str:
    """Extract text from a Reddit wiki page JSON response."""
    try:
        return data["data"]["content_md"]
    except (KeyError, TypeError):
        return ""


def _extract_reddit_comments(data: Any) -> str:
    """
    Recursively walk the Reddit listing JSON to collect:
        - the original post selftext
        - all comment bodies (depth-first)
    """
    texts: list[str] = []

    def _walk(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                _walk(item)
        elif isinstance(node, dict):
            kind = node.get("kind")
            d = node.get("data", {})
            if kind == "Listing":
                for child in d.get("children", []):
                    _walk(child)
            elif kind == "t3":  # Link / self-post
                body = d.get("selftext", "").strip()
                title = d.get("title", "").strip()
                if title:
                    texts.append(title)
                if body and body not in ("[removed]", "[deleted]"):
                    texts.append(body)
            elif kind == "t1":  # Comment
                body = d.get("body", "").strip()
                if body and body not in ("[removed]", "[deleted]"):
                    texts.append(body)
                # Recurse into replies
                replies = d.get("replies")
                if replies and isinstance(replies, dict):
                    _walk(replies)

    _walk(data)
    return "\n\n".join(texts)


def ingest_reddit(source: dict) -> str:
    """
    Load Reddit content from a local JSON file (if local_path is set and
    the file exists) or fetch it live via the Reddit JSON API.

    Returns the raw extracted text (not yet cleaned).
    """
    local_path = source.get("local_path")
    url = source["url"]

    # --- Try local file first ---
    if local_path and Path(local_path).exists():
        print(f"  [reddit] Loading from local file: {local_path}")
        with open(local_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        json_url = _reddit_json_url(url)
        print(f"  [reddit] Fetching: {json_url}")
        time.sleep(REDDIT_REQUEST_DELAY)
        response = requests.get(json_url, headers=REDDIT_HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
        # Optionally save to disk for reproducibility
        if local_path:
            Path(local_path).parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)
            print(f"  [reddit] Saved to {local_path}")

    # Detect wiki vs. thread
    if isinstance(data, dict) and "data" in data and "content_md" in data.get("data", {}):
        raw = _extract_reddit_wiki(data)
    else:
        raw = _extract_reddit_comments(data)

    return raw


# ---------------------------------------------------------------------------
# Plain-text ingestion
# ---------------------------------------------------------------------------

def ingest_txt(source: dict) -> str:
    """Load article content from a plain .txt file."""
    local_path = source.get("local_path")
    if not local_path or not Path(local_path).exists():
        raise FileNotFoundError(
            f"[txt] File not found for source {source['id']}: {local_path!r}\n"
            f"  → Copy-paste the article text into that file first."
        )
    print(f"  [txt] Loading: {local_path}")
    with open(local_path, "r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    # Try to split on paragraph, then sentence, then word, then character
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function=len,
)


def chunk_document(text: str, source: dict) -> list[dict]:
    """
    Split cleaned text into chunks and attach metadata to each chunk.

    Returns a list of dicts:
        {
            "chunk_id":    "<source_id>_<index>",
            "source_id":   int,
            "source_name": str,
            "source_type": str,
            "description": str,
            "url":         str,
            "chunk_index": int,
            "text":        str,
        }
    """
    chunks = splitter.split_text(text)
    results = []
    for i, chunk in enumerate(chunks):
        results.append(
            {
                "chunk_id": f"{source['id']}_{i}",
                "source_id": source["id"],
                "source_name": source["source_name"],
                "source_type": source["source_type"],
                "description": source["description"],
                "url": source["url"],
                "chunk_index": i,
                "text": chunk,
            }
        )
    return results


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(sources: list[dict] = SOURCES) -> list[dict]:
    """
    Run ingestion + cleaning + chunking for all sources.

    Returns a flat list of chunk dicts ready for embedding / vector store.
    """
    all_chunks: list[dict] = []

    for source in sources:
        src_id = source["id"]
        src_type = source["source_type"]
        print(f"\n[{src_id}] {source['description']} ({src_type})")

        try:
            if src_type == "reddit":
                raw = ingest_reddit(source)
            elif src_type == "txt":
                raw = ingest_txt(source)
            else:
                raise ValueError(f"Unknown source_type: {src_type!r}")

            if not raw.strip():
                print(f"  ⚠ No content extracted - skipping.")
                continue

            cleaned = _clean_text(raw)
            chunks = chunk_document(cleaned, source)
            all_chunks.extend(chunks)
            print(f"  ✓ {len(chunks)} chunks produced")

        except FileNotFoundError as exc:
            print(f"  ✗ {exc}")
        except requests.HTTPError as exc:
            print(f"  ✗ HTTP error: {exc}")
        except Exception as exc:  # noqa: BLE001
            print(f"  ✗ Unexpected error: {exc}")

    print(f"\n{'─'*50}")
    print(f"Total chunks: {len(all_chunks)}")
    return all_chunks


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # chunks = run_pipeline()
    with open("data/chunks.json", "r", encoding="utf-8") as fh:
        chunks = json.load(fh)
        
    # Quick preview
    # print("\n--- Sample chunks ---")
    # for chunk in chunks[:3]:
    #     print(
    #         f"\n[{chunk['chunk_id']}] {chunk['source_name']} | {chunk['description']}"
    #     )
    #     print(f"  chars: {len(chunk['text'])}")
    #     print(f"  text:  {chunk['text'][:120]}…")

    # Print 5 representative chunks
    import random
    sample = random.sample(chunks, min(5, len(chunks)))
    for chunk in sample:
        print(f"\n[{chunk['chunk_id']}] {chunk['source_name']} — {chunk['description']}")
        print(f"  {chunk['text']}")

    # Optionally persist to JSON for inspection / hand-off to next pipeline stage
    # out_path = Path("data/chunks.json")
    # out_path.parent.mkdir(parents=True, exist_ok=True)
    # with open(out_path, "w", encoding="utf-8") as fh:
    #     json.dump(chunks, fh, ensure_ascii=False, indent=2)
    # print(f"\nChunks saved to {out_path}")
