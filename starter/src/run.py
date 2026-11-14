"""Day 06 pipeline: Python 3.13 docs -> page units -> A/B/C chunks -> MiniLM -> Chroma.

Run from ``starter/``::

    python -m src.run prepare    # download check, extract corpus, page units, manifest
    python -m src.run validate   # locate every evidence quote -> gold pages (pre-run)
    python -m src.run ingest     # chunk + embed + upsert all strategies (twice: reload check)
    python -m src.run evaluate   # top-3 traces, Hit@1 / Evidence Hit@3, audit sheets
    python -m src.run all
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from . import chunking, ingestion
from .evaluation import evaluate_query, norm, summarize
from .models import DocumentPage

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "python-3.13-docs-text.zip"
CORPUS_DIR = ROOT / "data" / "corpus"
PAGES_FILE = ROOT / "data" / "pages.jsonl"
MANIFEST = ROOT / "data" / "manifest.json"
BENCH = ROOT / "benchmark" / "questions.json"
RESULTS = ROOT / "results"
CHROMA_DIR = ROOT / "starter" / "chroma_db"
MODEL = "sentence-transformers/all-MiniLM-L6-v2"

STRATEGIES = {
    "A": {"chunking": "fixed_size", "size": 500, "overlap": 50, "filter": False},
    "B": {"chunking": "by_section", "max_size": 1000, "overlap": 0, "filter": False},
    "C": {"chunking": "by_section", "max_size": 1000, "overlap": 0, "filter": True},
}


def log(msg: str) -> None:
    print(msg, flush=True)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------- prepare
def prepare() -> list[DocumentPage]:
    if not RAW.exists():
        RAW.parent.mkdir(parents=True, exist_ok=True)
        log(f"downloading {ingestion.ARCHIVE_URL}")
        urllib.request.urlretrieve(ingestion.ARCHIVE_URL, RAW)
    records = ingestion.extract_corpus(RAW, CORPUS_DIR)
    accessed = datetime.now(timezone.utc).date().isoformat()
    all_pages, errors, manifest_docs = [], [], []
    for rec in records:
        pages, errs = ingestion.load_document(rec)
        errors.extend(errs)
        all_pages.extend(pages)
        manifest_docs.append({
            "source_id": rec["document_id"],
            "title": pages[0].metadata["first_section"].split(" > ")[0] if pages else "",
            "source_path_or_url": pages[0].metadata["url"] if pages else "",
            "archive_member": f"{ingestion.ARCHIVE_PREFIX}{rec['rel']}.txt",
            "local_copy": str(rec["path"].relative_to(ROOT)).replace("\\", "/"),
            "doc_type": rec["doc_type"],
            "version": f"Python {ingestion.PYTHON_VERSION} documentation (text archive)",
            "license_or_permission": "PSF License Agreement for Python 3.13 (docs © 2001-2024 PSF); "
                                     "code examples under Zero-Clause BSD — see license.txt in archive",
            "accessed_at": accessed, "raw_sha256": rec["sha256"], "raw_bytes": rec["raw_bytes"],
            "pages": [{"page": p.page, "page_id": p.metadata["page_id"], "chars": len(p.text),
                       "first_section": p.metadata["first_section"],
                       "sections": [s["path"] for s in p.metadata["sections"]]} for p in pages],
            "page_count": len(pages), "chars": sum(len(p.text) for p in pages),
        })
    with PAGES_FILE.open("w", encoding="utf-8") as fh:
        for p in all_pages:
            fh.write(json.dumps({"document_id": p.document_id, "source": p.source, "page": p.page,
                                 "metadata": p.metadata, "text": p.text}, ensure_ascii=False) + "\n")
    short = [p.metadata["page_id"] for p in all_pages if len(p.text) < ingestion.MIN_PAGE_CHARS]
    write_json(MANIFEST, {
        "corpus": "Python 3.13 documentation — tutorial + library subset",
        "archive_url": ingestion.ARCHIVE_URL,
        "page_rule": f"No physical pages. Each document is split in reading order at headings; "
                     f"consecutive sections are merged until a unit has >= {ingestion.MIN_PAGE_CHARS} "
                     f"normalized chars (a short tail merges into the previous unit). "
                     f"All units are counted (the selected files contain no cover/TOC/blank pages).",
        "normalization": "UTF-8 decode, Unicode NFC, CRLF->LF, NBSP->space, tab->4 spaces, "
                         "strip trailing spaces, collapse 3+ newlines to 2",
        "total_documents": len(manifest_docs), "total_pages": len(all_pages),
        "total_chars": sum(len(p.text) for p in all_pages),
        "pages_below_min_chars": short, "errors": errors, "documents": manifest_docs,
    })
    write_json(RESULTS / "ingest_errors.json", {"errors": errors, "pages_below_min_chars": short})
    log(f"prepare: {len(manifest_docs)} docs, {len(all_pages)} page units, "
        f"{sum(len(p.text) for p in all_pages)} chars, errors={len(errors)}")
    return all_pages


def load_pages() -> list[DocumentPage]:
    pages = []
    with PAGES_FILE.open(encoding="utf-8") as fh:
        for line in fh:
            d = json.loads(line)
            pages.append(DocumentPage(d["document_id"], d["source"], d["page"], d["text"], d["metadata"]))
    return pages


# ---------------------------------------------------------------- validate
def benchmark_hash(bench: dict) -> str:
    """SHA-256 of questions/splits/answers/evidence/filters (excludes computed pages
    and timestamps) so a grader can check the set did not change after validation."""
    import hashlib
    core = [{k: v for k, v in q.items() if k != "gold"} |
            {"gold": [{"source_id": g["source_id"], "evidence_quote": g["evidence_quote"]}
                      for g in q["gold"]]} for q in bench["questions"]]
    return hashlib.sha256(json.dumps(core, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def validate() -> dict:
    """Locate each evidence quote in the normalized pages and record gold pages.
    Runs before any retrieval; fails loudly if a quote is missing."""
    pages = load_pages()
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    problems = []
    for q in bench["questions"]:
        for g in q["gold"]:
            found = [p.page for p in pages if p.document_id == g["source_id"]
                     and norm(g["evidence_quote"]) in norm(p.text)]
            if not found:
                problems.append(f"{q['id']}: evidence not found in {g['source_id']}")
            g["pages"] = found
        if q.get("filter"):
            vals = {p.metadata["doc_type"] for p in pages}
            if q["filter"].get("doc_type") not in vals:
                problems.append(f"{q['id']}: filter value not present in metadata")
    splits = [q["split"] for q in bench["questions"]]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    bench.setdefault("first_validated_at", bench.get("validated_at", now))  # never overwritten
    bench["validated_at"] = now  # last validation
    bench["benchmark_sha256"] = benchmark_hash(bench)
    bench["counts"] = {"dev": splits.count("dev"), "test": splits.count("test"),
                       "with_filter": sum(1 for q in bench["questions"] if q.get("filter")),
                       "test_with_filter": sum(1 for q in bench["questions"]
                                               if q.get("filter") and q["split"] == "test")}
    if problems:
        for p in problems:
            log("VALIDATION ERROR " + p)
        sys.exit(1)
    write_json(BENCH, bench)
    log(f"validate: OK {bench['counts']}")
    return bench


# ---------------------------------------------------------------- ingest
def build_chunks(strategy: str, pages: list[DocumentPage]):
    cfg = STRATEGIES[strategy]
    chunks = []
    for p in pages:
        if cfg["chunking"] == "fixed_size":
            chunks.extend(chunking.fixed_size(p, cfg["size"], cfg["overlap"], strategy))
        else:
            chunks.extend(chunking.by_section(p, cfg["max_size"], strategy))
    return chunks


def ingest(embedder, store) -> dict:
    pages = load_pages()
    stats = {}
    cache: dict[str, list[float]] = {}
    for strategy in STRATEGIES:
        t0 = time.perf_counter()
        chunks = build_chunks(strategy, pages)
        t_chunk = time.perf_counter() - t0
        texts = [c.text for c in chunks]
        t1 = time.perf_counter()
        key = "|".join(f"{c.document_id}{c.page}{c.metadata['content_hash']}" for c in chunks)
        if strategy == "C" and key in cache:  # identical chunks to B -> same vectors
            vectors, reused = cache[key], True
        else:
            vectors, reused = embedder.embed_documents(texts), False
            cache[key] = vectors
        t_embed = time.perf_counter() - t1
        t2 = time.perf_counter()
        first = store.upsert(strategy, chunks, vectors)
        t_store = time.perf_counter() - t2
        second = store.upsert(strategy, chunks, vectors)  # reload same version: must not grow
        lengths = [len(t) for t in texts]
        stats[strategy] = {
            **STRATEGIES[strategy], "chunk_count": len(chunks), "total_chars": sum(lengths),
            "approx_tokens_chars_div4": sum(lengths) // 4,
            "len_min": min(lengths), "len_median": int(statistics.median(lengths)),
            "len_mean": round(statistics.mean(lengths), 1), "len_max": max(lengths),
            "len_p90": sorted(lengths)[int(0.9 * len(lengths))],
            "over_model_window_256tok_est": sum(1 for x in lengths if x / 4 > embedder.max_seq_length),
            "time_chunk_s": round(t_chunk, 2), "time_embed_s": round(t_embed, 2),
            "time_store_s": round(t_store, 2), "vectors_reused_from_B": reused,
            "upsert_first": first, "upsert_reload": second,
            "reload_no_duplicates": second["after"] == len(chunks) and first["after"] == len(chunks),
            "cost_usd": 0.0,
        }
        log(f"ingest {strategy}: {len(chunks)} chunks, embed {t_embed:.1f}s, "
            f"reload {first['after']}->{second['after']}")
    write_json(RESULTS / "ingest_stats.json", {
        "embedding_model": embedder.model_name, "dimensions": embedder.dimensions,
        "max_seq_length_tokens": embedder.max_seq_length,
        "vector_store": f"chromadb {__import__('chromadb').__version__} PersistentClient",
        "store_path": str(CHROMA_DIR.relative_to(ROOT)).replace("\\", "/"),
        "metric": "cosine (HNSW, approximate)",
        "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "strategies": stats})
    return stats


# ---------------------------------------------------------------- evaluate
def evaluate(embedder, store) -> list[dict]:
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    sha = benchmark_hash(bench)
    if sha != bench.get("benchmark_sha256"):
        sys.exit("benchmark changed since last validate: run `python -m src.run validate` first")
    traces = []
    for strategy, cfg in STRATEGIES.items():
        for q in bench["questions"]:
            filters = q.get("filter") if cfg["filter"] else None
            t0 = time.perf_counter()
            qv = embedder.embed_query(q["question"])
            hits = store.search(strategy, qv, top_k=3, filters=filters)
            latency = time.perf_counter() - t0
            ev = evaluate_query(q, hits)
            traces.append({
                "strategy": strategy, "id": q["id"], "split": q["split"], "type": q["type"],
                "question": q["question"], "filter_applied": filters,
                "question_filter": q.get("filter"), "expected_answer": q["expected_answer"],
                "gold": q["gold"], "latency_s": round(latency, 4), "eval": ev,
                "top3": [{**h, "is_hit": f} for h, f in zip(hits, ev["hit_flags"])],
            })
    with (RESULTS / "traces.jsonl").open("w", encoding="utf-8") as fh:
        for t in traces:
            fh.write(json.dumps(t, ensure_ascii=False) + "\n")
    summary = summarize(traces)
    # filter compliance (automatic check of returned metadata vs question filter)
    for row in summary:
        sub = [t for t in traces if t["strategy"] == row["strategy"] and t["split"] == row["split"]
               and t["question_filter"]]
        ok = sum(all(h["metadata"]["doc_type"] == t["question_filter"]["doc_type"] for h in t["top3"])
                 for t in sub)
        row["filter_questions"] = len(sub)
        row["filter_compliant_top3"] = ok
    write_json(RESULTS / "summary.json", {"benchmark_sha256": sha,
                                          "benchmark_first_validated_at": bench.get("first_validated_at"),
                                          "evaluated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                          "rows": summary})
    with (RESULTS / "per_question.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["strategy", "id", "split", "type", "filter", "hit1", "hit3",
                    "gold_page_in_top3", "top1_chunk", "top1_score", "top_pages"])
        for t in traces:
            w.writerow([t["strategy"], t["id"], t["split"], t["type"],
                        json.dumps(t["question_filter"]) if t["question_filter"] else "",
                        int(t["eval"]["hit1"]), int(t["eval"]["hit3"]), int(t["eval"]["gold_page_in_top3"]),
                        t["top3"][0]["chunk_id"], t["top3"][0]["score"],
                        " | ".join(f"{h['metadata']['document_id']}#p{h['metadata']['page']}" for h in t["top3"])])
    for row in summary:
        log(f"{row['strategy']} {row['split']}: Hit@1 {row['hit1']}/{row['N']}  "
            f"Hit@3 {row['hit3']}/{row['N']}  filter {row['filter_compliant_top3']}/{row['filter_questions']}")
    return traces


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["prepare", "validate", "ingest", "evaluate", "all"])
    step = ap.parse_args().step
    if step in ("prepare", "all"):
        prepare()
    if step in ("validate", "all"):
        validate()
    if step in ("ingest", "evaluate", "all"):
        from .embeddings import SentenceTransformerEmbedder
        from .store import ChromaStore
        embedder = SentenceTransformerEmbedder(MODEL)
        store = ChromaStore(CHROMA_DIR, embedder.dimensions, embedder.model_name)
        if step in ("ingest", "all"):
            ingest(embedder, store)
        if step in ("evaluate", "all"):
            evaluate(embedder, store)


if __name__ == "__main__":
    main()
