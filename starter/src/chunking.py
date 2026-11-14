"""Fixed-size (strategy A) and structure-aware (strategies B/C) chunking.

Both chunkers work inside one page unit, so every chunk maps to exactly one
``document_id`` + ``page``. Chunk IDs are deterministic (strategy, document,
page, ordinal) so re-ingesting the same version overwrites instead of
duplicating.
"""
from __future__ import annotations

import hashlib

from .ingestion import parse_sections
from .models import Chunk, DocumentPage


def _section_at(page: DocumentPage, offset: int) -> str:
    pos = 0
    current = page.metadata["sections"][0]["path"]
    for sec in page.metadata["sections"]:
        if pos > offset:
            break
        current = sec["path"]
        pos += sec["chars"] + 2  # sections are joined with "\n\n"
    return current


def _make(strategy: str, page: DocumentPage, n: int, text: str, section: str,
          start: int, end: int) -> Chunk:
    return Chunk(
        chunk_id=f"{strategy}:{page.document_id}:p{page.page:03d}:c{n:03d}",
        document_id=page.document_id, source=page.source, page=page.page, text=text,
        metadata={
            "page_id": page.metadata["page_id"], "section": section,
            "doc_type": page.metadata["doc_type"], "url": page.metadata["url"],
            "python_version": page.metadata["python_version"],
            "char_start": start, "char_end": end, "chars": len(text),
            "content_hash": hashlib.sha256(text.encode()).hexdigest()[:16],
        })


def fixed_size(page: DocumentPage, size: int = 500, overlap: int = 50,
               strategy: str = "A") -> list[Chunk]:
    """Character windows of ``size`` with ``overlap``; no structural awareness."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    text, chunks, start, n = page.text, [], 0, 0
    while start < len(text):
        end = min(start + size, len(text))
        piece = text[start:end]
        if piece.strip():
            chunks.append(_make(strategy, page, n, piece, _section_at(page, start), start, end))
            n += 1
        if end == len(text):
            break
        start = end - overlap
    return chunks


def _split_long(paragraph: str, max_size: int) -> list[str]:
    """Split an oversized paragraph on line boundaries (falls back to hard cut)."""
    parts, buf = [], ""
    for line in paragraph.split("\n"):
        while len(line) > max_size:
            if buf:
                parts.append(buf)
                buf = ""
            parts.append(line[:max_size])
            line = line[max_size:]
        if buf and len(buf) + 1 + len(line) > max_size:
            parts.append(buf)
            buf = line
        else:
            buf = f"{buf}\n{line}" if buf else line
    if buf:
        parts.append(buf)
    return parts


def by_section(page: DocumentPage, max_size: int = 1000, strategy: str = "B") -> list[Chunk]:
    """Heading-aware chunking: never cross a heading; pack whole paragraphs up to
    ``max_size``; prefix each chunk with its heading path for context."""
    chunks: list[Chunk] = []
    n = 0
    offset = 0
    for sec in parse_sections(page.text):
        if not sec.path:  # page starts with a continuation of a long section
            sec.path = page.metadata["sections"][0]["path"]
        lines = sec.text.split("\n")
        # drop the heading + underline from the body; the path is used as prefix
        body = "\n".join(lines[2:]).strip("\n") if sec.title else sec.text
        sec_start = page.text.find(sec.text, offset)
        offset = max(offset, sec_start)
        if not body.strip():
            continue
        paragraphs: list[str] = []
        for para in body.split("\n\n"):
            if not para.strip():
                continue
            paragraphs.extend(_split_long(para, max_size) if len(para) > max_size else [para])
        prefix = f"[{sec.path}]\n" if sec.path else ""
        buf: list[str] = []
        for para in paragraphs:
            if buf and len(prefix) + len("\n\n".join(buf + [para])) > max_size:
                chunks.append(_make(strategy, page, n, prefix + "\n\n".join(buf), sec.path,
                                    sec_start, sec_start + len(sec.text)))
                n += 1
                buf = []
            buf.append(para)
        if buf:
            chunks.append(_make(strategy, page, n, prefix + "\n\n".join(buf), sec.path,
                                sec_start, sec_start + len(sec.text)))
            n += 1
    return chunks
