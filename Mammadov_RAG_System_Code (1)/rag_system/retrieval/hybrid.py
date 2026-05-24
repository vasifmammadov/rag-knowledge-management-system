"""
retrieval/hybrid.py
Module 3 — Hybrid Retrieval: RRF fusion + reranking + query enhancement.
Cross-encoder replaced with score-based reranker for offline demo.
"""
import re
from collections import defaultdict

RRF_K = 60

def detect_language(query: str) -> str:
    try:
        from langdetect import detect
        return detect(query)
    except Exception:
        return 'en'

def enhance_query(query: str, acronym_dict: dict = None) -> str:
    if not acronym_dict:
        acronym_dict = {
            'RAG': 'Retrieval-Augmented Generation',
            'LLM': 'Large Language Model',
            'NLP': 'Natural Language Processing',
            'AI':  'Artificial Intelligence',
            'KMS': 'Knowledge Management System',
            'LOTO': 'Lock-Out Tag-Out',
            'MRR': 'Mean Reciprocal Rank',
        }
    def replace(m):
        acr = m.group(0)
        return f'{acr} ({acronym_dict[acr]})' if acr in acronym_dict else acr
    expanded = re.sub(r'\b[A-Z]{2,5}\b', replace, query)
    return ' '.join(expanded.split())

def reciprocal_rank_fusion(dense_results, sparse_results, top_k=20):
    rrf_scores  = defaultdict(float)
    chunk_index = {}
    for rank, result in enumerate(dense_results, start=1):
        cid = result['chunk_id']
        rrf_scores[cid]  += 1.0 / (RRF_K + rank)
        chunk_index[cid]  = result
    for rank, result in enumerate(sparse_results, start=1):
        cid = result['chunk_id']
        rrf_scores[cid]  += 1.0 / (RRF_K + rank)
        if cid not in chunk_index:
            chunk_index[cid] = result
    sorted_ids = sorted(rrf_scores, key=rrf_scores.__getitem__, reverse=True)
    fused = []
    for cid in sorted_ids[:top_k]:
        rec = dict(chunk_index[cid])
        rec['rrf_score'] = rrf_scores[cid]
        fused.append(rec)
    return fused

class Reranker:
    """
    Lightweight keyword-overlap reranker for offline demo.
    Full system uses cross-encoder/ms-marco-MiniLM-L-6-v2.
    Interface and output format identical.
    """
    def __init__(self):
        print("  [Reranker] Keyword-overlap reranker ready (offline mode)")

    def rerank(self, query: str, candidates: list, top_k: int = 10) -> list:
        query_words = set(re.findall(r'\w+', query.lower()))
        scored = []
        for cand in candidates:
            text_words = set(re.findall(r'\w+', cand['text'].lower()))
            overlap = len(query_words & text_words)
            # Combine with RRF score
            rrf = cand.get('rrf_score', 0)
            score = overlap * 0.1 + rrf * 10
            rec = dict(cand)
            rec['rerank_score'] = round(score, 4)
            scored.append(rec)
        scored.sort(key=lambda x: x['rerank_score'], reverse=True)
        return scored[:top_k]
