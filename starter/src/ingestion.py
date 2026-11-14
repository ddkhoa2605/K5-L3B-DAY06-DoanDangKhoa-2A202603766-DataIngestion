"""Read and normalize the Python 3.13 documentation (plain-text build).

The official text archive has no physical pages, so each document is split in
reading order into *page units*: consecutive heading-delimited sections are
merged until the unit holds at least ``MIN_PAGE_CHARS`` normalized characters
(GUIDE.md §1). A section is never split across two units, so every unit starts
on a heading and can be traced back to it.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
import zipfile
from dataclasses import dataclass
from pathlib import Path

from .models import DocumentPage

PYTHON_VERSION = "3.13"
ARCHIVE_URL = "https://docs.python.org/3.13/archives/python-3.13-docs-text.zip"
ARCHIVE_PREFIX = "python-3.13-docs-text/"
MIN_PAGE_CHARS = 1500

# document_id -> (path inside archive without .txt, doc_type)
CORPUS: dict[str, tuple[str, str]] = {
    "tut-controlflow": ("tutorial/controlflow", "tutorial"),
    "tut-datastructures": ("tutorial/datastructures", "tutorial"),
    "tut-errors": ("tutorial/errors", "tutorial"),
    "tut-modules": ("tutorial/modules", "tutorial"),
    "tut-inputoutput": ("tutorial/inputoutput", "tutorial"),
    "tut-venv": ("tutorial/venv", "tutorial"),
    "lib-json": ("library/json", "library"),
    "lib-csv": ("library/csv", "library"),
    "lib-functools": ("library/functools", "library"),
    "lib-venv": ("library/venv", "library"),
}

# Sphinx text writer underline characters, in heading-level order.
_UNDERLINE = re.compile(r"^([*=\-~^\"#+])\1{2,}$")
_LEVEL = {"*": 1, "=": 2, "-": 3}


@dataclass
class Section:
    level: int
    title: str
    path: str      # "8. Errors and Exceptions > 8.3. Handling Exceptions"
    text: str      # heading lines + body


def normalize_text(text: str) -> str:
    """NFC-normalize, unify newlines/spaces; keep blank lines and indentation (code)."""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace(" ", " ").replace("\t", "    ")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def extract_corpus(archive: Path, out_dir: Path) -> list[dict]:
    """Copy the selected files out of the archive; return raw-file records."""
    out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    with zipfile.ZipFile(archive) as zf:
        for doc_id, (rel, doc_type) in CORPUS.items():
            raw = zf.read(f"{ARCHIVE_PREFIX}{rel}.txt")
            target = out_dir / f"{rel.replace('/', '__')}.txt"
            target.write_bytes(raw)
            records.append({"document_id": doc_id, "rel": rel, "doc_type": doc_type,
                            "path": target, "sha256": hashlib.sha256(raw).hexdigest(),
                            "raw_bytes": len(raw)})
    return records


def parse_sections(text: str) -> list[Section]:
    """Split normalized text at Sphinx-style underlined headings."""
    lines = text.split("\n")
    heads: list[tuple[int, int, str]] = []  # (line index, level, title)
    for i in range(len(lines) - 1):
        title, under = lines[i], lines[i + 1]
        m = _UNDERLINE.match(under)
        if (m and title.strip() and not title.startswith(" ")
                and len(under) >= len(title.strip()) and not _UNDERLINE.match(title)):
            heads.append((i, _LEVEL.get(m.group(1), 4), title.strip()))
    sections: list[Section] = []
    stack: list[tuple[int, str]] = []
    if not heads or heads[0][0] > 0:
        end = heads[0][0] if heads else len(lines)
        sections.append(Section(0, "", "", "\n".join(lines[:end])))
    for n, (start, level, title) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, title))
        path = " > ".join(t for _, t in stack)
        sections.append(Section(level, title, path, "\n".join(lines[start:end]).strip("\n")))
    return [s for s in sections if s.text.strip()]


LONG_SECTION_CHARS = 3000


def _split_long_sections(sections: list[Section]) -> list[Section]:
    """A section longer than LONG_SECTION_CHARS (e.g. a library page with no
    sub-headings) is cut at paragraph boundaries into parts of >= MIN_PAGE_CHARS.
    Continuation parts keep the section path (marked " (cont.)")."""
    out: list[Section] = []
    for sec in sections:
        if len(sec.text) <= LONG_SECTION_CHARS:
            out.append(sec)
            continue
        parts: list[str] = []
        buf: list[str] = []
        for para in sec.text.split("\n\n"):
            buf.append(para)
            if len("\n\n".join(buf)) >= MIN_PAGE_CHARS:
                parts.append("\n\n".join(buf))
                buf = []
        if buf:
            if parts:
                parts[-1] = parts[-1] + "\n\n" + "\n\n".join(buf)
            else:
                parts.append("\n\n".join(buf))
        for i, part in enumerate(parts):
            path = sec.path if i == 0 else f"{sec.path} (cont.)"
            out.append(Section(sec.level, sec.title, path, part))
    return out


def split_pages(document_id: str, source: str, doc_type: str, url: str,
                text: str) -> tuple[list[DocumentPage], list[str]]:
    """Merge consecutive sections into page units of >= MIN_PAGE_CHARS chars."""
    errors: list[str] = []
    sections = _split_long_sections(parse_sections(text))
    groups: list[list[Section]] = []
    current: list[Section] = []
    for sec in sections:
        current.append(sec)
        if sum(len(s.text) for s in current) >= MIN_PAGE_CHARS:
            groups.append(current)
            current = []
    if current:  # short tail joins the previous unit so every unit is >= MIN
        if groups:
            groups[-1].extend(current)
        else:
            groups.append(current)
            errors.append(f"{document_id}: whole document shorter than {MIN_PAGE_CHARS} chars")
    pages = []
    for n, group in enumerate(groups, start=1):
        body = "\n\n".join(s.text for s in group)
        if not body.strip():
            errors.append(f"{document_id} page {n}: empty")
            continue
        pages.append(DocumentPage(
            document_id=document_id, source=source, page=n, text=body,
            metadata={
                "doc_type": doc_type, "url": url, "python_version": PYTHON_VERSION,
                "page_id": f"{document_id}#p{n:03d}",
                "first_section": group[0].path,
                "sections": [{"path": s.path, "level": s.level, "chars": len(s.text)} for s in group],
            }))
    return pages, errors


def load_document(record: dict) -> tuple[list[DocumentPage], list[str]]:
    errors: list[str] = []
    raw = record["path"].read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:  # record, then keep going with replacement chars
        errors.append(f"{record['document_id']}: utf-8 decode error {exc}")
        text = raw.decode("utf-8", errors="replace")
    text = normalize_text(text)
    rel = record["rel"]
    source = f"{ARCHIVE_PREFIX}{rel}.txt"
    url = f"https://docs.python.org/{PYTHON_VERSION}/{rel}.html"
    pages, page_errors = split_pages(record["document_id"], source, record["doc_type"], url, text)
    return pages, errors + page_errors
