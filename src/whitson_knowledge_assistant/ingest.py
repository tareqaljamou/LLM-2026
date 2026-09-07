from __future__ import annotations

import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[2]
SOURCES_FILE = ROOT / "data" / "sources.json"
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def clean_text(html: str) -> str:
    """Extract readable text from an HTML page."""
    soup = BeautifulSoup(html, "html.parser")

    for element in soup(
        ["script", "style", "noscript", "header", "footer", "nav", "form"]
    ):
        element.decompose()

    text = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def make_chunks(text: str) -> list[str]:
    """Split text into overlapping character-based chunks."""
    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def ingest_source(title: str, url: str) -> list[dict]:
    print(f"Downloading: {title}")

    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "WhitsonKnowledgeAssistant/0.1"},
    )
    response.raise_for_status()

    text = clean_text(response.text)

    raw_file = RAW_DIR / f"{len(list(RAW_DIR.glob('*.html'))):03d}.html"
    raw_file.write_text(response.text, encoding="utf-8")

    chunks = make_chunks(text)

    return [
        {
            "chunk_id": f"{title}-{index}",
            "title": title,
            "url": url,
            "text": chunk,
        }
        for index, chunk in enumerate(chunks)
    ]


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    sources = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))

    all_chunks: list[dict] = []

    for source in sources:
        try:
            all_chunks.extend(
                ingest_source(
                    title=source["title"],
                    url=source["url"],
                )
            )
        except requests.RequestException as exc:
            print(f"Skipping {source['url']}: {exc}")

    output_file = PROCESSED_DIR / "chunks.json"
    output_file.write_text(
        json.dumps(all_chunks, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Saved {len(all_chunks)} chunks to {output_file}")


if __name__ == "__main__":
    main()
