"""Automatic retrieval metrics (Hit@1, Evidence Hit@3) with full traces.

A retrieved chunk is a hit only if it belongs to a gold (document_id, page)
AND contains the whole evidence quote (case/whitespace-insensitive). Manual
coherence / grounding labels are NOT inferred here.
"""
from __future__ import annotations

import re
from typing import Any


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def chunk_is_hit(hit: dict[str, Any], golds: list[dict[str, Any]]) -> bool:
    meta, body = hit["metadata"], norm(hit["text"])
    for g in golds:
        if (meta["document_id"] == g["source_id"] and meta["page"] in g["pages"]
                and norm(g["evidence_quote"]) in body):
            return True
    return False


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    flags = [chunk_is_hit(h, question["gold"]) for h in hits]
    # diagnostic only: right page retrieved but evidence split / partially present
    page_only = [any(h["metadata"]["document_id"] == g["source_id"] and h["metadata"]["page"] in g["pages"]
                     for g in question["gold"]) for h in hits]
    return {"hit_flags": flags, "hit1": bool(flags and flags[0]), "hit3": any(flags[:3]),
            "gold_page_in_top3": any(page_only[:3])}


def summarize(traces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for strategy in sorted({t["strategy"] for t in traces}):
        for split in ("dev", "test"):
            sub = [t for t in traces if t["strategy"] == strategy and t["split"] == split]
            if not sub:
                continue
            n = len(sub)
            h1 = sum(t["eval"]["hit1"] for t in sub)
            h3 = sum(t["eval"]["hit3"] for t in sub)
            pg = sum(t["eval"]["gold_page_in_top3"] for t in sub)
            rows.append({"strategy": strategy, "split": split, "N": n,
                         "hit1": h1, "hit3": h3, "gold_page_top3": pg,
                         "hit1_rate": round(h1 / n, 3), "hit3_rate": round(h3 / n, 3)})
    return rows
