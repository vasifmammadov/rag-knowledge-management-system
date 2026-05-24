"""
embedding/bm25_store.py
Module 2 — BM25 Sparse Index with bilingual tokenisation (EN + LV).
"""
import re
from rank_bm25 import BM25Okapi

EN_STOPWORDS = {'the','a','an','is','in','of','to','and','or','for','with','be','are','was','has','by'}
LV_STOPWORDS = {'un','ir','ka','ar','no','par','tā','šis','būt','vai','tas','šī','kā','tiek'}
STOPWORDS    = EN_STOPWORDS | LV_STOPWORDS


def tokenize(text: str) -> list:
    """Bilingual tokeniser: handles ASCII + Latvian diacritics."""
    tokens = re.findall(r'[a-zA-ZāčēģīķļņšūžĀČĒĢĪĶĻŅŠŪŽ]+', text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


class BM25Store:
    def __init__(self):
        self.corpus_tokens: list = []
        self.chunk_records: list = []
        self.bm25 = None

    def build(self, chunk_records: list):
        for r in chunk_records:
            self.corpus_tokens.append(tokenize(r['text']))
            self.chunk_records.append(r)
        self.bm25 = BM25Okapi(self.corpus_tokens)

    def search(self, query: str, k: int = 20) -> list:
        if not self.bm25:
            return []
        scores  = self.bm25.get_scores(tokenize(query))
        top_idx = scores.argsort()[::-1][:k]
        results = []
        for i in top_idx:
            if scores[i] > 0:
                rec = dict(self.chunk_records[i])
                rec['bm25_score'] = float(scores[i])
                results.append(rec)
        return results
