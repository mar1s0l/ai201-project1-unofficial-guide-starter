"""
query.py
--------
Generation step for UCLA Dining RAG pipeline.

Ties together:
    - HybridRetriever  (BM25 + ChromaDB)
    - Groq             (llama-3.3-70b-versatile)

The LLM is instructed to answer strictly from the retrieved context.
Returns a dict:  { "answer": str, "sources": list[str] }

Usage:
    from query import ask
    result = ask("Which dining hall has the best vegan options?")
    print(result["answer"])
    print(result["sources"])
"""

from __future__ import annotations

import os
from dotenv import load_dotenv

from groq import Groq
from retrieve import HybridRetriever

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GROQ_MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 512

SYSTEM_PROMPT = """You are a helpful assistant that answers questions about UCLA dining.
You must answer using ONLY the context chunks provided below.
If the answer cannot be found in the context, say "I don't have enough information to answer that."
Do not use any outside knowledge. Do not make anything up.
Be concise and direct."""

# ---------------------------------------------------------------------------
# Initialise clients (once at import time)
# ---------------------------------------------------------------------------

load_dotenv()
_retriever = HybridRetriever()
_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
MAX_HISTORY_TURNS = 4


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

def _build_prompt(question: str, chunks: list[dict]) -> str:
    """
    Assemble the user-turn prompt from retrieved chunks.
    Each chunk is labelled with its source so the model can attribute answers.
    """
    context_blocks = []
    for i, chunk in enumerate(chunks, start=1):
        meta = chunk["metadata"]
        context_blocks.append(
            f"[{i}] Source: {meta['source_name']} — {meta['description']}\n"
            f"URL: {meta['url']}\n"
            f"{chunk['text']}"
        )

    context = "\n\n---\n\n".join(context_blocks)

    return (
        f"Context:\n\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer the question using only the context above. "
        "Format your response as:\n"
        "Answer: <your answer>\n"
        "Sources: <comma-separated list of source names and URLs you used>"
    )


# ---------------------------------------------------------------------------
# Source deduplication
# ---------------------------------------------------------------------------

def _extract_sources(chunks: list[dict]) -> list[str]:
    """
    Return a deduplicated list of source strings from the retrieved chunks,
    formatted as  'SourceName — Description (URL)'.
    """
    seen: set[str] = set()
    sources: list[str] = []
    for chunk in chunks:
        meta = chunk["metadata"]
        entry = f"{meta['source_name']} — {meta['description']} ({meta['url']})"
        if entry not in seen:
            seen.add(entry)
            sources.append(entry)
    return sources


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

_conversation_history = []

def ask(question: str) -> dict[str, str | list[str]]:
    """
    End-to-end RAG query.

    Parameters
    ----------
    question : str
        The user's natural-language question.

    Returns
    -------
    dict with keys:
        "answer"  : str         — LLM answer grounded in retrieved context
        "sources" : list[str]   — deduplicated source attribution strings
    """
    # global _conversation_history
    
    # 1. Retrieve relevant chunks via hybrid search
    chunks = _retriever.retrieve(question)

    if not chunks:
        return {
            "answer": "I don't have enough information to answer that.",
            "sources": [],
        }

    # 2. Build prompt
    prompt = _build_prompt(question, chunks)
    
    # 2.5 Add the new user turn to history, but trim history first
    if len(_conversation_history) >= MAX_HISTORY_TURNS * 2:
        _conversation_history[:] = _conversation_history[-(MAX_HISTORY_TURNS * 2):]
        
    _conversation_history.append({"role": "user", "content": prompt})

    # 3. Call Groq
    response = _groq.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *_conversation_history,
        ],
    )

    raw_answer = response.choices[0].message.content.strip()

    # 4. Parse out just the Answer: block if the model followed the format,
    #    otherwise return the full response
    if "Answer:" in raw_answer:
        answer_text = raw_answer.split("Answer:")[-1].split("Sources:")[0].strip()
    else:
        answer_text = raw_answer
        
    # 4.5 Add the LLM's turn to history
    _conversation_history.append({"role": "assistant", "content": answer_text})

    # 5. Use our own source list (more reliable than parsing the LLM output)
    sources = _extract_sources(chunks)

    return {
        "answer": answer_text,
        "sources": sources,
    }

def reset_conversation():
    _conversation_history.clear()
