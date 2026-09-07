## Architecture

```text
Public Whitson sources
        |
        v
Source ingestion
        |
        v
HTML cleaning and text extraction
        |
        v
Text chunking
        |
        v
Local JSON knowledge base
        |
        v
Keyword retrieval
        |
        v
OpenAI answer generation
        |
        v
Citations and user interface

whitson-knowledge-assistant/
├── data/
│   └── sources.json
├── docs/
│   └── project-charter.md
├── src/
│   └── whitson_knowledge_assistant/
│       ├── __init__.py
│       ├── answer.py
│       ├── app.py
│       ├── chat.py
│       ├── ingest.py
│       └── retrieve.py
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock
