from __future__ import annotations
import argparse, hashlib, json, re, urllib.request
from pathlib import Path
INDEX_URL="https://code.claude.com/docs/llms.txt"
PATTERN=re.compile(r"^- \[[^\]]+\]\((https://code\.claude\.com/docs/([^)]+))\):", re.M)

def parse_index(text: str) -> list[str]:
    return [path for _, path in PATTERN.findall(text)]

def fetch_index(url: str=INDEX_URL) -> bytes:
    with urllib.request.urlopen(url, timeout=20) as response:
        return response.read()

def manufacture_lock(raw: bytes, observed_at: str) -> dict:
    paths=parse_index(raw.decode("utf-8"))
    if not paths:
        raise ValueError("official Claude Code index yielded zero documents")
    return {"schema_version":1,"observed_at":observed_at,"index_url":INDEX_URL,"index_sha256":hashlib.sha256(raw).hexdigest(),"document_paths":paths}

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--observed-at",required=True,help="explicit ISO-8601 observation time; never inferred")
    ap.add_argument("--output",type=Path,default=Path("src/claudecodegym/data/official_docs.lock.json"))
    ns=ap.parse_args()
    ns.output.write_text(json.dumps(manufacture_lock(fetch_index(),ns.observed_at),indent=2)+"\n")
    print(ns.output)
if __name__=="__main__": main()
