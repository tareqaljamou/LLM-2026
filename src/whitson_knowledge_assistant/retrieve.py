from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHUNKS_FILE = ROOT / "data" / "processed" / "chunks.json"


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"\b[a-zA-Z0-9]{3,}\b", text.lower()))


def load_chunks() -> list[dict]:
    return json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))


def search(query: str, limit: int = 5) -> list[dict]:
    query_terms = tokenize(query)
    results = []

    for chunk in load_chunks():
        chunk_terms = tokenize(chunk["text"])
        score = len(query_terms & chunk_terms)

        if score > 0:
            results.append((score, chunk))

    results.sort(key=lambda item: item[0], reverse=True)

    return [
        {
            **chunk,
            "score": score,
        }
        for score, chunk in results[:limit]
    ]


if __name__ == "__main__":
    results = search("What is nodal analysis?")

    for result in results:
        print("=" * 80)
        print("Score:", result["score"])
        print("Title:", result["title"])
        print("URL:", result["url"])
        print(result["text"][:500])
