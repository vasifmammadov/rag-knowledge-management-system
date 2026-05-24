"""
ingestion/parser.py
Module 1 — Multi-format document parser.
Supports plain text (.txt) and structured dictionaries.
In the full system: PDF via PyMuPDF, DOCX via python-docx.
"""
import re
import uuid
from dataclasses import dataclass, field
from typing import List
from langdetect import detect


@dataclass
class ParsedDocument:
    doc_id: str
    title: str
    language: str
    sections: List[dict]   # [{'heading': str, 'level': int, 'text': str}]
    metadata: dict


def detect_language(text: str) -> str:
    try:
        return detect(text[:500])
    except Exception:
        return "en"


def parse_text(content: str, title: str, metadata: dict = None) -> ParsedDocument:
    """
    Parse plain text into sections by detecting heading patterns.
    Headings detected as: lines in ALL CAPS, lines ending with ':', 
    or lines starting with a number like '1.' / '1.1'.
    """
    doc_id = str(uuid.uuid4())[:8]
    lines = content.strip().split('\n')
    sections = []
    current = {'heading': title, 'level': 1, 'text': ''}

    heading_pattern = re.compile(
        r'^(\d+\.[\d.]*\s+\S|[A-Z][A-Z\s]{3,}$|.{3,50}:$)'
    )

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if heading_pattern.match(line) and len(line) < 80:
            if current['text'].strip():
                sections.append(current)
            level = 2 if re.match(r'^\d+\.\d+', line) else 1
            current = {'heading': line.rstrip(':'), 'level': level, 'text': ''}
        else:
            current['text'] += ' ' + line

    if current['text'].strip():
        sections.append(current)

    lang = detect_language(content)
    return ParsedDocument(
        doc_id=doc_id,
        title=title,
        language=lang,
        sections=sections,
        metadata=metadata or {}
    )
