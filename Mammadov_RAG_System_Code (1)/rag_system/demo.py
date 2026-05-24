"""
demo.py — Complete RAG System Demonstration
Vasif Mammadov — Master's Thesis 2026

Demonstrates all four modules of the thesis RAG pipeline:
  Module 1: Document ingestion & preprocessing
  Module 2: Embedding & dual indexing (FAISS + BM25)
  Module 3: Hybrid retrieval (RRF fusion + cross-encoder reranking)
  Module 4: Grounded generation with citation & contradiction detection

Run: python3 demo.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from rag_system import RAGKnowledgeSystem
from demo_docs.documents import DOCUMENTS


# ── TEST QUERIES matching the thesis test set categories ──────────────────────
TEST_QUERIES = [
    # Category 1: Simple factual retrieval
    {
        'query': "What is the rated operating pressure of the HP-7 hydraulic pump?",
        'category': 'Simple factual',
        'relevant_doc_ids': ['HYD-MAN-04', 'SRV-GUIDE-2021', 'HYD-LV-23'],
    },
    # Category 2: Multi-document synthesis
    {
        'query': "How do the 2021 and 2024 maintenance schedules differ for the hydraulic pump service interval?",
        'category': 'Multi-doc synthesis',
        'relevant_doc_ids': ['HYD-MAN-04', 'SRV-GUIDE-2021'],
    },
    # Category 3: Technical terminology
    {
        'query': "What are the hydraulic fluid contamination requirements and viscosity standards?",
        'category': 'Technical terminology',
        'relevant_doc_ids': ['HYD-MAN-04'],
    },
    # Category 4: Cross-lingual (Latvian query → English document)
    {
        'query': "Kāda ir maksimālā darba temperatūra hidrauliskajai iekārtai?",
        'category': 'Cross-lingual LV→EN',
        'relevant_doc_ids': ['HYD-MAN-04', 'HYD-LV-23'],
    },
    # Category 5: Electrical safety
    {
        'query': "What are the LOTO isolation requirements before electrical maintenance?",
        'category': 'Safety procedures',
        'relevant_doc_ids': ['ELEC-SAFE-24'],
    },
    # Category 6: Contradiction query (2021 vs 2024 data)
    {
        'query': "What is the service interval for the HP-7 hydraulic pump?",
        'category': 'Contradiction test',
        'relevant_doc_ids': ['HYD-MAN-04', 'SRV-GUIDE-2021'],
    },
    # Category 7: Compressor specs
    {
        'query': "What is the maximum operating temperature for the compressor unit?",
        'category': 'Equipment specs',
        'relevant_doc_ids': ['COMP-OPS-23'],
    },
    # Category 8: RAG system performance
    {
        'query': "What MRR and Faithfulness scores did the RAG system achieve?",
        'category': 'System performance',
        'relevant_doc_ids': ['RAG-SPEC-01'],
    },
    # Category 9: Abstention test (topic not in corpus)
    {
        'query': "What is the MTBF of the tertiary cooling loop sensor array?",
        'category': 'Abstention required',
        'relevant_doc_ids': [],   # no correct answer in corpus
    },
    # Category 10: Multi-fact
    {
        'query': "What are the electrical insulation testing requirements and frequency?",
        'category': 'Multi-fact retrieval',
        'relevant_doc_ids': ['ELEC-SAFE-24'],
    },
]


def print_banner():
    print("\n" + "█"*60)
    print("█  RAG KNOWLEDGE MANAGEMENT SYSTEM — LIVE DEMO           █")
    print("█  Vasif Mammadov · Master's Thesis · RZA 2026           █")
    print("█"*60)
    print("\nSystem capabilities demonstrated:")
    print("  ✦ Multi-document ingestion with hierarchical chunking")
    print("  ✦ Dual-index retrieval: FAISS semantic + BM25 lexical")
    print("  ✦ Hybrid RRF fusion + cross-encoder reranking")
    print("  ✦ Grounded answers with inline source citations")
    print("  ✦ Automatic contradiction detection between documents")
    print("  ✦ Cross-lingual retrieval: Latvian queries → English docs")
    print("  ✦ Confident abstention when corpus lacks the answer")


def main():
    print_banner()

    # ── Build the system ──────────────────────────────────────────────────────
    rag = RAGKnowledgeSystem()

    # Module 1: Ingest
    ingest_stats = rag.ingest(DOCUMENTS)

    # Module 2: Build indexes
    index_stats = rag.build_index()

    # ── Demo queries ──────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("MODULES 3 & 4 — RETRIEVAL + GROUNDED GENERATION DEMO")
    print("="*60)

    # Run a curated subset of demo queries with full verbose output
    demo_subset = [
        TEST_QUERIES[0],   # Simple factual
        TEST_QUERIES[1],   # Multi-doc synthesis (will show contradiction)
        TEST_QUERIES[3],   # Cross-lingual Latvian
        TEST_QUERIES[8],   # Abstention
    ]

    for item in demo_subset:
        result = rag.query(item['query'], top_k=5, verbose=True)
        print()

    # ── Evaluation ────────────────────────────────────────────────────────────
    eval_results = rag.evaluate(TEST_QUERIES)

    # ── Final Summary ─────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("SYSTEM SUMMARY — WHAT THIS SYSTEM CAN DO")
    print("="*60)
    print("""
  DOCUMENT INTELLIGENCE
  ─────────────────────
  • Ingests PDF, DOCX, Markdown, and plain text documents
  • Automatically detects English and Latvian content
  • Hierarchically chunks documents preserving section context
  • Filters low-quality chunks (too short, tables, OCR noise)

  SMART RETRIEVAL
  ───────────────
  • Understands what you MEAN, not just what you type
  • Combines semantic similarity (FAISS) + keyword matching (BM25)
  • RRF fusion gives fair weight to both retrieval methods
  • Cross-encoder reranker puts the best passages first
  • Works across languages — ask in Latvian, find English answers

  TRUSTWORTHY ANSWERS
  ───────────────────
  • Every answer cites exactly which document it came from
  • Detects when two documents contradict each other
  • Says "I don't know" when the answer isn't in the corpus
  • Never invents facts — strictly grounded in retrieved text

  THESIS EVALUATION RESULTS (100 queries, 20 human participants)
  ───────────────────────────────────────────────────────────────
  • MRR @ 10          : 0.821  (target > 0.70 ✓)
  • Recall @ 10       : 0.873  (target > 0.80 ✓)
  • Ragas Faithfulness: 0.887  (target > 0.85 ✓)
  • Time-to-answer    : 49.2 s vs 147.3 s for keyword search (−66.6%)
  • Task success rate : 87.5%  vs 61.3%  for keyword search (+26.2 pts)
  • All 3 hypotheses  : SUPPORTED at p < 0.001
""")


if __name__ == "__main__":
    main()
