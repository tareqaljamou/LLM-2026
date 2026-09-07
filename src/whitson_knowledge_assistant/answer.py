from __future__ import annotations

import os
import re

from dotenv import load_dotenv
from openai import OpenAI

from whitson_knowledge_assistant.retrieve import search

load_dotenv()

def clean_url(url: str) -> str:
    """Convert Markdown-style URLs into plain URLs."""
    if "](" in url:
        return url.split("](", 1)[1].rstrip(")")
    return url.strip()


def prepare_sources(results: list[dict]) -> list[dict]:
    """
    Clean URLs and remove duplicate sources.
    """
    sources = []
    seen = set()

    for result in results:
        source = {
            **result,
            "url": clean_url(result["url"]),
        }

        source_key = (source["title"], source["url"])

        if source_key not in seen:
            sources.append(source)
            seen.add(source_key)

    return sources


def build_context(results: list[dict]) -> str:
    """
    Build the context sent to the language model.
    """
    parts = []

    for index, result in enumerate(results, start=1):
        parts.append(
            f"""Source [{index}]
Title: {result["title"]}
URL: {result["url"]}

Content:
{result["text"]}
"""
        )

    return "\n\n".join(parts)


def build_sources_section(results: list[dict]) -> str:
    """
    Build a clean source list for the final answer.
    """
    lines = ["\n\nSources:"]

    for index, result in enumerate(results, start=1):
        lines.append(
            f"[{index}] {result['title']} — {result['url']}"
        )

    return "\n".join(lines)


def answer_question(question: str, limit: int = 5) -> str:
    """
    Retrieve relevant content and generate a grounded answer.
    """
    results = search(question, limit=limit)
    results = prepare_sources(results)

    if not results:
        return (
            "I don't know based on the indexed public Whitson sources. "
            "No relevant source material was retrieved."
        )

    context = build_context(results)

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a technical knowledge assistant for petroleum "
                    "engineering. Answer only from the supplied sources. "
                    "Do not use outside knowledge. "
                    "If the sources do not contain enough information, say: "
                    "'I don't know based on the indexed sources.' "
                    "Do not invent equations, values, recommendations, or "
                    "product capabilities. "
                    "Use source citations in the form [1], [2], and so on. "
                    "Only cite sources that support the statement. "
                    "Do not create a Sources section because the application "
                    "will add it automatically."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n"
                    f"Context:\n{context}"
                ),
            },
        ],
    )

    answer = response.choices[0].message.content

    if not answer:
        answer = "No answer was generated."

    return answer + build_sources_section(results)


if __name__ == "__main__":
    print(answer_question("What is nodal analysis?"))
