"""
embedding/embedder.py
Module 2 — Local TF-IDF + LSA embedding (offline demo).
Full system: intfloat/multilingual-e5-large via sentence-transformers.
"""
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

DIM = 64  # reduced for small corpus; full system: 1024


class Embedder:
    def __init__(self):
        print("  [Embedder] TF-IDF + LSA pipeline (local, offline demo mode)")
        self.tfidf  = TfidfVectorizer(analyzer='word', ngram_range=(1,2),
                                      max_features=5000, sublinear_tf=True)
        self.svd    = TruncatedSVD(n_components=DIM, random_state=42)
        self.fitted = False
        print("  [Embedder] Ready.")

    def _fit_and_encode(self, texts: list) -> np.ndarray:
        tfidf_mat = self.tfidf.fit_transform(texts)
        # Ensure n_components <= n_features
        n_feat = tfidf_mat.shape[1]
        self.svd.n_components = min(DIM, n_feat - 1)
        vecs = self.svd.fit_transform(tfidf_mat)
        self.fitted = True
        return normalize(vecs, norm='l2').astype('float32')

    def _encode(self, texts: list) -> np.ndarray:
        tfidf_mat = self.tfidf.transform(texts)
        vecs = self.svd.transform(tfidf_mat)
        return normalize(vecs, norm='l2').astype('float32')

    def embed_passages(self, texts: list) -> np.ndarray:
        vecs = self._fit_and_encode(texts)
        self.actual_dim = vecs.shape[1]
        return vecs

    def embed_query(self, query: str) -> np.ndarray:
        return self._encode([query])[0]


class FaissStore:
    def __init__(self, dim: int = DIM):
        self.dim    = dim
        self.id_map = {}
        self.index  = None

    def build(self, embeddings: np.ndarray, chunk_records: list):
        n, d        = embeddings.shape
        self.dim    = d
        self.index  = faiss.IndexFlatIP(d)
        self.index.add(embeddings)
        for i, record in enumerate(chunk_records):
            self.id_map[i] = record
        print(f"  [FAISS] IndexFlatIP: {n} vectors × {d}d")

    def search(self, query_vec: np.ndarray, k: int = 20) -> list:
        k = min(k, len(self.id_map))
        q = query_vec.reshape(1, -1)
        D, I = self.index.search(q, k)
        results = []
        for j, idx in enumerate(I[0]):
            if idx >= 0 and idx in self.id_map:
                rec = dict(self.id_map[idx])
                rec['dense_score'] = float(D[0][j])
                results.append(rec)
        return results
