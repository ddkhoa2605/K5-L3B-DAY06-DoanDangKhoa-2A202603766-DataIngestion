"""Metadata audit of test top-3 + aggregation of manual labels.

Metadata check per retrieved record (test questions x top-3 x strategy):
  document_id exists in manifest; source == manifest archive member;
  page exists and its normalized text contains the chunk body (so source+page
  really locate the text); doc_type == manifest doc_type.
  -> "required_ok" when all hold.
  section: also checked whether it is the FULL heading path from the manifest
  (supplementary field, reported separately).

Run from starter/:  python scripts/audit_summary.py
"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "results" / "audit"


def norm(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


manifest = json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))
docs = {d["source_id"]: d for d in manifest["documents"]}
pages = {}
for line in (ROOT / "data" / "pages.jsonl").open(encoding="utf-8"):
    p = json.loads(line)
    pages[(p["document_id"], p["page"])] = p
traces = [json.loads(l) for l in (ROOT / "results" / "traces.jsonl").open(encoding="utf-8")]

rows = []
for t in traces:
    if t["split"] != "test":
        continue
    for h in t["top3"]:
        m = h["metadata"]
        body = h["text"]
        if body.startswith("[") and "]\n" in body:  # B/C heading prefix is not source text
            body = body.split("]\n", 1)[1]
        d = docs.get(m["document_id"])
        page = pages.get((m["document_id"], m["page"]))
        checks = {
            "doc_ok": d is not None,
            "source_ok": bool(d) and m["source"] == d["archive_member"],
            "page_ok": bool(page) and norm(body) in norm(page["text"]),
            "doc_type_ok": bool(d) and m["doc_type"] == d["doc_type"],
        }
        full_paths = {s["path"] for s in page["metadata"]["sections"]} if page else set()
        section_full = m["section"] in full_paths
        flt = t["question_filter"]
        rows.append({
            "strategy": t["strategy"], "id": t["id"], "rank": h["rank"], "chunk_id": h["chunk_id"],
            "document_id": m["document_id"], "page": m["page"], "doc_type": m["doc_type"],
            "section": m["section"], **{k: int(v) for k, v in checks.items()},
            "required_ok": int(all(checks.values())), "section_full_path": int(section_full),
            "question_filter": json.dumps(flt) if flt else "",
            "in_filter_scope": "" if not flt else int(m["doc_type"] == flt["doc_type"]),
            "note": "" if section_full else "section is page-local heading only (parent path lost)",
        })
with (AUDIT / "metadata_audit.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

summary = defaultdict(dict)
for s in ("A", "B", "C"):
    r = [x for x in rows if x["strategy"] == s]
    summary[s]["metadata_required_ok"] = f"{sum(x['required_ok'] for x in r)}/{len(r)}"
    summary[s]["section_full_path"] = f"{sum(x['section_full_path'] for x in r)}/{len(r)}"
    fq = defaultdict(list)
    for x in r:
        if x["question_filter"]:
            fq[x["id"]].append(x["in_filter_scope"])
    summary[s]["test_filter_compliant_questions"] = f"{sum(all(v) for v in fq.values())}/{len(fq)}"

for name, key in (("coherence_labels.csv", "position"), ("grounding_labels.csv", "id")):
    with (AUDIT / name).open(encoding="utf-8") as fh:
        labels = list(csv.DictReader(fh))
    for s in ("A", "B", "C"):
        sc = [int(x["score_0_2"]) for x in labels if x["strategy"] == s]
        c = Counter(sc)
        summary[s][name.split("_")[0]] = {
            "n": len(sc), "mean_0_2": round(sum(sc) / len(sc), 2),
            "count_0": c[0], "count_1": c[1], "count_2": c[2]}

(ROOT / "results" / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
