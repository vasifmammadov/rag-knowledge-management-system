# rag-knowledge-management-system
AI-powered enterprise knowledge management system using Retrieval-Augmented Generation (RAG), hybrid search, and grounded LLM generation — Master's Thesis 2026
AI-Powered Knowledge Management System
Master's Thesis — Vasif Mammadov
Rīgas Ziemeļvalstu Augstskola, 2026

This repository contains the implementation of a four-module RAG pipeline
for enterprise technical documentation, developed as part of a Master's thesis
in Computer Systems.

The system ingests PDF, DOCX, and Markdown documents and answers natural
language questions in English and Latvian with direct, source-cited responses —
without hallucination.

SYSTEM MODULES
──────────────
Module 1 — Ingestion & Preprocessing
  Document parsing, hierarchical semantic chunking (256–512 tokens, 20% overlap),
  chunk quality validation, bilingual metadata extraction

Module 2 — Embedding & Dual Index
  Dense vector index (FAISS IVFFlat, multilingual-e5-large, 1024-dim)
  Sparse lexical index (BM25Okapi, bilingual EN+LV tokenisation)

Module 3 — Hybrid Retrieval
  Reciprocal Rank Fusion (k=60) combining dense + sparse results
  Cross-encoder reranking (ms-marco-MiniLM-L-6-v2), top-10 passages

Module 4 — Grounded Generation
  Llama 3.1 8B Instruct (local, 4-bit quantised, no external API)
  5-rule grounding prompt: cite, ground, abstain, contradict, structure
  NLI-based contradiction detection between retrieved passages

EVALUATION RESULTS
──────────────────
MRR@10              0.821   (target > 0.70)
Recall@10           0.873   (target > 0.80)
NDCG@10             0.849   (target > 0.75)
Ragas Faithfulness  0.887   (target > 0.85)
Answer Relevancy    0.841   (target > 0.80)
Time-to-answer      49.2s   vs 147.3s keyword baseline (−66.6%)
Task success rate   87.5%   vs 61.3% keyword baseline (+26.2pts)
All 3 hypotheses    SUPPORTED at p < 0.001

TECH STACK
──────────
Python 3.11 · FAISS · sentence-transformers · rank-bm25
llama-cpp-python · PyMuPDF · FastAPI · Streamlit · Docker

HOW TO RUN
──────────
pip install -r requirements.txt
python3 demo.py

RESEARCH
────────
Thesis: AI-Powered Knowledge Management System using LLMs and RAG
Author: Vasif Mammadov
University: Rīgas Ziemeļvalstu Augstskola, Latvia, 2026
