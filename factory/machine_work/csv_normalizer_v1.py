#!/usr/bin/env python3
"""Deterministic CSV normalizer for machine-compatible data work.

Reads a CSV, writes a normalized CSV copy, and emits a JSON report.
The source file is never modified.
"""
from __future__ import annotations
import csv, json, sys, hashlib
from pathlib import Path

MISSING = {"", "na", "n/a", "null", "none"}

def norm_text(v: str) -> str:
    return " ".join(v.strip().split())

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    if len(sys.argv) != 4:
        print("usage: csv_normalizer_v1.py INPUT.csv OUTPUT.csv REPORT.json", file=sys.stderr)
        return 2
    src, out, report = map(Path, sys.argv[1:])
    rows_changed = 0
    cells_changed = 0
    missing_standardized = 0
    with src.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV must contain a header row")
        headers = [norm_text(h) for h in reader.fieldnames]
        data = []
        for row in reader:
            changed = False
            clean = {}
            for old_h, new_h in zip(reader.fieldnames, headers):
                raw = row.get(old_h, "") or ""
                val = norm_text(raw)
                if val.lower() in MISSING:
                    if val != "":
                        missing_standardized += 1
                    val = ""
                if val != raw:
                    cells_changed += 1
                    changed = True
                clean[new_h] = val
            if changed:
                rows_changed += 1
            data.append(clean)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    result = {
        "version": "1.0",
        "source_sha256": sha256(src),
        "rows": len(data),
        "columns": len(headers),
        "rows_changed": rows_changed,
        "cells_changed": cells_changed,
        "missing_markers_standardized": missing_standardized,
        "output": str(out),
        "source_modified": False,
    }
    report.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
