"""Check re-ingest behaviour on a throw-away Chroma directory (not the real index).

1. ingest tut-venv with strategy B            -> N chunks
2. ingest the same version again               -> still N (no duplicates)
3. simulate a changed source (last page cut)   -> stale chunk IDs deleted, count = new N
Uses the real embedding model. Run from starter/: python scripts/test_reingest.py
"""
import shutil
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "starter"))
from src.embeddings import SentenceTransformerEmbedder  # noqa: E402
from src.run import MODEL, build_chunks, load_pages  # noqa: E402
from src.store import ChromaStore  # noqa: E402

tmp = Path(tempfile.mkdtemp(prefix="chroma_reingest_"))
try:
    emb = SentenceTransformerEmbedder(MODEL)
    store = ChromaStore(tmp, emb.dimensions, emb.model_name)
    pages = [p for p in load_pages() if p.document_id == "tut-venv"]
    chunks = build_chunks("B", pages)
    vecs = emb.embed_documents([c.text for c in chunks])
    r1 = store.upsert("B", chunks, vecs)
    r2 = store.upsert("B", chunks, vecs)
    changed = pages[:-1] + [replace(pages[-1], text=pages[-1].text[: len(pages[-1].text) // 3])]
    chunks2 = build_chunks("B", changed)
    r3 = store.upsert("B", chunks2, emb.embed_documents([c.text for c in chunks2]))
    print(f"first ingest : {r1}  (chunks={len(chunks)})")
    print(f"same version : {r2}  duplicates={'NO' if r2['after'] == len(chunks) else 'YES'}")
    print(f"changed doc  : {r3}  (new chunks={len(chunks2)}) "
          f"stale removed={'OK' if r3['after'] == len(chunks2) else 'FAIL'}")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
