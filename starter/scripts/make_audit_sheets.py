"""Build audit sheets for manual labeling (does NOT assign labels).

Coherence sample rule (fixed before labeling, independent of scores): for each of
the 10 documents, take the position at the middle of page unit 2, snapped to the
start of that line. For each strategy, the chunk covering that position is shown.
(C uses exactly the same chunks as B, so its coherence sample is identical.)

Test sheet: every test question x strategy x top-3 with metadata + text, for the
metadata-correctness audit and grounding labels.

Run from starter/:  python scripts/make_audit_sheets.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "starter"))
from src.run import STRATEGIES, build_chunks, load_pages  # noqa: E402

OUT = ROOT / "results" / "audit"
OUT.mkdir(parents=True, exist_ok=True)

pages = load_pages()
chunks = {s: build_chunks(s, pages) for s in ("A", "B")}
lines = ["# Coherence samples (auto-generated, labels in coherence_labels.csv)\n"]
for doc in sorted({p.document_id for p in pages}):
    page = next(p for p in pages if p.document_id == doc and p.page == 2)
    mid = len(page.text) // 2
    mid = page.text.rfind("\n", 0, mid) + 1
    probe = page.text[mid:mid + 40].strip() or page.text[mid:mid + 80].strip()
    lines.append(f"\n## POS {doc}#p002 @char {mid}: `{probe}`\n")
    for s in ("A", "B"):
        cover = [c for c in chunks[s] if c.document_id == doc and c.page == 2
                 and (c.metadata["char_start"] <= mid < c.metadata["char_end"] if s == "A"
                      else probe.split("\n")[0] in c.text)]
        c = cover[0] if cover else None
        lines.append(f"\n### {s}: {c.chunk_id if c else 'NOT FOUND'}\n")
        if c:
            lines.append("```text\n" + c.text + "\n```\n")
(OUT / "coherence_samples.md").write_text("\n".join(lines), encoding="utf-8")

traces = [json.loads(l) for l in (ROOT / "results" / "traces.jsonl").open(encoding="utf-8")]
out = ["# Test top-3 sheet (auto-generated, labels in metadata_audit.csv / grounding_labels.csv)\n"]
for t in traces:
    if t["split"] != "test":
        continue
    out.append(f"\n## {t['strategy']} {t['id']} filter_applied={t['filter_applied']}\n")
    out.append(f"Q: {t['question']}\nGold: {[(g['source_id'], g['pages']) for g in t['gold']]}\n")
    for h in t["top3"]:
        m = h["metadata"]
        out.append(f"\n### rank {h['rank']} {h['chunk_id']} score={h['score']} hit={h['is_hit']}\n"
                   f"source={m['source']} page={m['page']} page_id={m['page_id']} "
                   f"doc_type={m['doc_type']} section={m['section']}\n")
        out.append("```text\n" + h["text"] + "\n```\n")
(OUT / "test_top3_sheet.md").write_text("\n".join(out), encoding="utf-8")
print("wrote", OUT / "coherence_samples.md", OUT / "test_top3_sheet.md")
