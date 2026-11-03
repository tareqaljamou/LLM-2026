Whitson Knowledge Assistant

A small RAG assistant that answers petroleum engineering questions from public Whitson documentation, with numbered citations. If the sources don't contain the answer, it says so instead of guessing.

Built for petroleum engineers and data people who want quick, source-backed answers. Whitson is a petroleum engineering software and consulting company known for PVT and reservoir fluid tools. Made as a project for the DataTalks.Club LLM Zoomcamp 2026.

This prototype uses public sources only. It does not use private Whitson documents or customer data.

How it works
text
Public Whitson sources (data/sources.json)
        |
        v
Ingestion + HTML cleaning  -->  chunks of ~1200 characters (200 overlap)
        |
        v
Local JSON knowledge base (data/processed/chunks.json)
        |
        v
Keyword retrieval (top 5 chunks)
        |
        v
OpenAI answer, using only the retrieved text, with [1], [2] citations
        |
        v
Streamlit app or command-line chat
Setup

You need uv and an OpenAI API key.

bash
git clone https://github.com/tareqaljamou/LLM-2026.git
cd LLM-2026

uv sync                          # install dependencies
cp .env.example .env             # then edit .env and add your OPENAI_API_KEY

uv run python -m whitson_knowledge_assistant.ingest      # download and index the sources
uv run streamlit run src/whitson_knowledge_assistant/app.py   # web app
# or the terminal version:
uv run python -m whitson_knowledge_assistant.chat

Run the tests and the evaluation:

bash
uv run pytest
uv run python evaluation/run_evaluation.py
Results

The evaluation script (evaluation/run_evaluation.py) checks that the assistant answers questions the sources cover, and declines questions they don't. It uses the question list in evaluation/questions.json.

<!-- Fill in after you run the script, using the real output: -->

Result: X of Y questions behaved as expected (model: gpt-4o-mini, date: DD Month 2026).

This test only checks answer versus decline. It does not yet measure whether each citation supports its statement, so treat it as a basic sanity check.

Limitations
Keyword retrieval only. No embeddings yet, so questions worded differently from the source text can be missed.
Few sources. It indexes only the pages listed in data/sources.json.
Answers can still be wrong. The model is told to answer only from the retrieved text, but this is not guaranteed. Check the cited sources for anything important.
Small evaluation set. Citation accuracy is not measured yet.
Next steps
Add embedding-based retrieval and compare it with keyword search.
Add more sources and a larger question set.
Measure citation accuracy.
Screenshots
Answer with citations

Whitson Knowledge Assistant demo

Declining an unsupported question

Whitson Knowledge Assistant declining an unsupported question

Project structure
text
LLM-2026/
├── data/sources.json
├── docs/project-charter.md
├── evaluation/          # questions.json and run_evaluation.py
├── screenshots/
├── src/whitson_knowledge_assistant/
│   ├── ingest.py        # download, clean, chunk
│   ├── retrieve.py      # keyword search
│   ├── answer.py        # prompt, OpenAI call, citations
│   ├── chat.py          # terminal chat
│   └── app.py           # Streamlit app
├── tests/
├── .env.example
└── pyproject.toml
License

MIT
