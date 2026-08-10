#!/usr/bin/env python3
"""Batch orchestration layer for machine-compatible CSV quality jobs.

Discovers CSV files, runs the existing deterministic data_quality_worker_v2.py
against each one, and emits a machine-readable batch manifest. Source files are
never modified.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("input_dir")
    p.add_argument("output_dir")
    p.add_argument("--worker", default="data_quality_worker_v2.py")
    args = p.parse_args()

    src = Path(args.input_dir)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    worker = Path(args.worker)
    files = sorted(src.glob("*.csv"))

    manifest = {
        "version": "1.0",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "input_dir": str(src.resolve()),
        "output_dir": str(out.resolve()),
        "jobs": [],
    }

    for f in files:
        report = out / f"{f.stem}.quality.json"
        cmd = [sys.executable, str(worker), str(f), "--json-out", str(report)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        manifest["jobs"].append({
            "input": str(f),
            "report": str(report),
            "exit_code": proc.returncode,
            "status": "ok" if proc.returncode == 0 else "review",
            "stderr": proc.stderr[-1000:],
        })

    manifest["finished_at"] = datetime.now(timezone.utc).isoformat()
    manifest["total_jobs"] = len(manifest["jobs"])
    manifest["ok_jobs"] = sum(j["status"] == "ok" for j in manifest["jobs"])
    manifest["review_jobs"] = manifest["total_jobs"] - manifest["ok_jobs"]
    manifest_path = out / "batch_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0 if manifest["review_jobs"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
