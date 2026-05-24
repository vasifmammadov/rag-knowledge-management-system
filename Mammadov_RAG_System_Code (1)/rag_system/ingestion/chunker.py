"""
ingestion/chunker.py
Module 1 — Hierarchical semantic chunker.
Splits sections into token-aware chunks with configurable overlap.
"""
import re
import uuid
from typing import List

MAX_TOKENS = 200    # reduced for demo (thesis uses 512)
OVERLAP_FRAC = 0.20


def simple_tokenize(text: str) -> List[str]:
    """Whitespace tokeniser (mirrors the thesis tokeniser logic)."""
    return text.split()


def chunk_section(section: dict, doc_meta: dict) -> List[dict]:
    """
    Stage 1: sentence-split the section text.
    Stage 2: greedy merge into chunks ≤ MAX_TOKENS with 20% overlap.
    Stage 3: inject metadata into each chunk record.
    """
    # Stage 1 — sentence splitting (simplified; thesis uses NLTK punkt)
    sentences = re.split(r'(?<=[.!?])\s+', section['text'].strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []
    buf: List[str] = []
    buf_tokens = 0

    for sent in sentences:
        t = len(simple_tokenize(sent))
        if buf_tokens + t > MAX_TOKENS and buf:
            chunks.append(_make_chunk(buf, section, doc_meta))
            # Stage 2 — retain overlap window
            overlap_target = int(MAX_TOKENS * OVERLAP_FRAC)
            while buf and buf_tokens > overlap_target:
                removed = buf.pop(0)
                buf_tokens -= len(simple_tokenize(removed))
        buf.append(sent)
        buf_tokens += t

    if buf:
        chunks.append(_make_chunk(buf, section, doc_meta))

    return chunks


def _make_chunk(sentences: List[str], section: dict, doc_meta: dict) -> dict:
    text = ' '.join(sentences)
    return {
        'chunk_id': str(uuid.uuid4())[:12],
        'text': text,
        'doc_id': doc_meta.get('doc_id', 'unknown'),
        'title': doc_meta.get('title', ''),
        'section': section['heading'],
        'level': section['level'],
        'language': doc_meta.get('language', 'en'),
        'access_level': doc_meta.get('access_level', 'public'),
        'token_count': len(simple_tokenize(text)),
    }
