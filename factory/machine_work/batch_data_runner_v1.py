#!/usr/bin/env python3
"""Batch runner for machine-compatible CSV jobs.

Discovers CSV files in an input directory, normalizes each into an output directory,
and writes a batch manifest. Source files are never modified.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: batch_data_runner_v1.py INPUT_DIR OUTPUT_DIR NORMALIZER.py", file=sys.stderr)
        return 2
    src_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    normalizer = Path(sys.argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)
    jobs=[]
    for src in sorted(src_dir.glob("*.csv")):
        cleaned = out_dir / f"{src.stem}.clean.csv"
        report = out_dir / f"{src.stem}.report.json"
        proc = subprocess.run([sys.executable, str(normalizer), str(src), str(cleaned), str(report)], capture_output=True, text=True)
        jobs.append({
            "source": str(src),
            "output": str(cleaned),
            "report": str(report),
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        })
    manifest = {"version":"1.0","job_count":len(jobs),"succeeded":sum(j['returncode']==0 for j in jobs),"failed":sum(j['returncode']!=0 for j in jobs),"jobs":jobs}
    (out_dir / "batch_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({k:manifest[k] for k in ['job_count','succeeded','failed']}))
    return 0 if manifest['failed']==0 else 1

if __name__ == '__main__':
    raise SystemExit(main())
