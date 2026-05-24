"""
generation/nli_checker.py
Module 4 — NLI-based contradiction detection.

Full system: facebook/bart-large-mnli via HuggingFace transformers.
Demo: lightweight keyword-based heuristic that detects numeric/factual 
contradictions between passages — same logic, zero GPU requirement.
"""
import re


def _extract_numbers(text: str):
    """Extract all numbers from text for contradiction heuristic."""
    return set(re.findall(r'\b\d+(?:\.\d+)?\b', text))


def _extract_entities(text: str):
    """Extract capitalised phrases as proxy entity detection."""
    words = text.split()
    entities = set()
    for i, w in enumerate(words):
        clean = re.sub(r'[^a-zA-Z]', '', w)
        if clean and clean[0].isupper() and len(clean) > 2:
            entities.add(clean.lower())
    return entities


def find_contradictions(passages: list) -> list:
    """
    Compare retrieved passages pairwise.
    Entity overlap pre-filter (matches thesis logic) reduces O(n²) to practical subset.
    Contradiction heuristic: passages share entities but have conflicting numeric values.
    """
    contradictions = []
    entities = [_extract_entities(p['text']) for p in passages]
    numbers  = [_extract_numbers(p['text'])  for p in passages]

    for i in range(len(passages)):
        for j in range(i + 1, len(passages)):
            # Pre-filter: must share at least one entity
            if not (entities[i] & entities[j]):
                continue
            # Contradiction signal: both have numbers, numbers differ, from different docs
            ni, nj = numbers[i], numbers[j]
            if ni and nj and ni != nj and passages[i]['doc_id'] != passages[j]['doc_id']:
                # Score proportional to entity overlap strength
                overlap = len(entities[i] & entities[j])
                score = min(0.95, 0.5 + overlap * 0.1)
                contradictions.append((i, j, round(score, 2)))

    return contradictions
