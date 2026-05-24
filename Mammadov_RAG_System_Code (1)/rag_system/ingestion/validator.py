"""
ingestion/validator.py
Module 1 — Chunk quality validation.
Three filters: minimum length, alphabetic ratio, repetition detection.
"""
from typing import Tuple

MIN_TOKENS  = 8
MIN_ALPHA   = 0.55
MAX_REPFRAC = 0.30


def validate_chunk(chunk: dict) -> Tuple[bool, str]:
    text = chunk.get('text', '')
    tokens = text.split()

    # Filter 1 — too short
    if len(tokens) < MIN_TOKENS:
        return False, 'too_short'

    # Filter 2 — low alphabetic ratio (tables, OCR noise)
    if len(text) == 0:
        return False, 'empty'
    alpha_ratio = sum(c.isalpha() for c in text) / len(text)
    if alpha_ratio < MIN_ALPHA:
        return False, 'low_alpha'

    # Filter 3 — repetitive trigrams (OCR artefacts)
    if len(tokens) >= 3:
        trigrams = [tuple(tokens[i:i+3]) for i in range(len(tokens) - 2)]
        if trigrams:
            most_freq = max(trigrams.count(t) for t in set(trigrams))
            if most_freq / len(trigrams) > MAX_REPFRAC:
                return False, 'repetitive'

    return True, 'ok'


def validate_corpus(chunks: list) -> Tuple[list, dict]:
    valid, stats = [], {'too_short': 0, 'low_alpha': 0, 'repetitive': 0, 'ok': 0}
    for chunk in chunks:
        ok, reason = validate_chunk(chunk)
        stats[reason] = stats.get(reason, 0) + 1
        if ok:
            valid.append(chunk)
    return valid, stats
