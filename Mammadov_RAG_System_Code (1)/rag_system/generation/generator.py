"""
generation/generator.py
Module 4 — Grounded Generation Layer.

In the full system: Llama 3.1 8B Instruct via llama-cpp-python (local GPU).
For this demo: rule-based grounded answer builder that strictly follows 
the same 5-rule prompt structure — no hallucination possible because 
it only extracts from retrieved passages.

The SYSTEM_PROMPT and build_prompt() functions are identical to the thesis.
"""

CONFIDENCE_THRESHOLD = 0.25   # minimum rerank_score to attempt an answer

SYSTEM_PROMPT = """You are a precise knowledge assistant for an enterprise
documentation system. Answer the user's question using ONLY the context
passages provided. Follow these rules without exception:

1. GROUNDING: Base every statement exclusively on the provided passages.
   Do not use prior knowledge or make inferences beyond what is stated.

2. CITATION: After each factual claim, append [Source: <doc_id>, <section>].
   If multiple passages support a claim, cite all of them.

3. ABSTENTION: If passages do not contain enough information, state:
   'The available documentation does not provide a complete answer.'
   Then describe what related information was found.

4. CONTRADICTION: If passages contradict each other, present both
   perspectives and note the discrepancy explicitly, referencing
   document dates where available.

5. STRUCTURE: Respond in clear paragraphs. End with a 'Sources consulted'
   section listing all cited documents."""


def build_prompt(query: str, passages: list) -> str:
    context = '\n\n'.join(
        f"[{p['doc_id']} | {p['section']}]\n{p['text']}"
        for p in passages
    )
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"CONTEXT PASSAGES:\n{context}\n\n"
        f"QUESTION: {query}\n\nANSWER:"
    )


def grounded_generate(query: str, passages: list, contradictions: list) -> dict:
    """
    Grounded answer builder.
    Extracts the most relevant sentences from top passages and assembles
    a cited, structured response — strictly from retrieved context.
    """
    if not passages:
        return {
            'answer': "The available documentation does not provide a complete answer to this question.",
            'confidence': 'low',
            'sources': [],
        }

    top_score = passages[0].get('rerank_score', passages[0].get('rrf_score', 0))
    if top_score < CONFIDENCE_THRESHOLD:
        related = passages[0]['section'] if passages else 'unknown section'
        return {
            'answer': (
                f"The available documentation does not provide a complete answer "
                f"to this question. Related information was found in '{related}'."
            ),
            'confidence': 'low',
            'sources': [],
        }

    # Build grounded answer from top passages
    answer_parts = []
    cited_sources = []
    query_words = set(query.lower().split())

    for i, passage in enumerate(passages[:5]):
        doc_id  = passage['doc_id']
        section = passage['section']
        text    = passage['text']

        # Find the most query-relevant sentences
        sentences = [s.strip() for s in text.replace('  ', ' ').split('. ') if len(s.strip()) > 20]
        scored = []
        for sent in sentences:
            sent_words = set(sent.lower().split())
            overlap = len(query_words & sent_words) / max(len(query_words), 1)
            scored.append((overlap, sent))
        scored.sort(reverse=True)

        best = [s for _, s in scored[:2] if s]
        if best:
            part = ' '.join(best)
            if not part.endswith('.'):
                part += '.'
            answer_parts.append(f"{part} [Source: {doc_id}, {section}]")
            cited_sources.append({'doc_id': doc_id, 'section': section,
                                   'title': passage.get('title',''),
                                   'score': round(top_score, 3)})

    # Contradiction warning
    contradiction_note = ""
    if contradictions:
        i, j, score = contradictions[0]
        s1 = passages[i]['section'] if i < len(passages) else '?'
        s2 = passages[j]['section'] if j < len(passages) else '?'
        contradiction_note = (
            f"\n\n⚠ CONTRADICTION DETECTED (confidence {score:.2f}): "
            f"Information in '{s1}' appears to conflict with information in '{s2}'. "
            f"Please consult both source documents directly to determine the authoritative version."
        )

    full_answer = ' '.join(answer_parts) + contradiction_note

    # Sources section
    seen = set()
    unique_sources = []
    for s in cited_sources:
        key = (s['doc_id'], s['section'])
        if key not in seen:
            seen.add(key)
            unique_sources.append(s)

    sources_text = "\n\nSources consulted:\n" + '\n'.join(
        f"  [{i+1}] {s['doc_id']} — {s['section']} (relevance: {s['score']})"
        for i, s in enumerate(unique_sources)
    )

    return {
        'answer': full_answer + sources_text,
        'confidence': 'high' if top_score > 0.4 else 'medium',
        'sources': unique_sources,
    }
