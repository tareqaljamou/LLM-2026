# Whitson AI Knowledge Navigator

## Project Status

MVP development

## Problem

Whitson already provides a large technical knowledge ecosystem
including public documentation, manuals, training material, and
technical resources.

The challenge is not simply the absence of information. The challenge
is helping an engineer quickly discover relevant information, connect
related concepts across documents, and understand the documented
workflow without losing source traceability.

## Project Objective

Build a citation-first Retrieval-Augmented Generation (RAG) prototype
that provides an AI interface over publicly available Whitson technical
knowledge.

The system should help users:

1. Find relevant Whitson documentation.
2. Understand technical concepts.
3. Connect information across multiple sources.
4. Navigate to the original documentation.
5. Distinguish documented information from unsupported conclusions.

## Target Users

Primary users:

- Petroleum engineers
- Reservoir engineers
- Production engineers
- PVT engineers
- Engineers learning Whitson software
- Technical users who need to navigate Whitson documentation

## Core User Questions

Examples:

- What is CCE?
- What is the purpose of EOS tuning?
- What is RTA?
- How does nodal analysis work?
- Where is gas-lift optimization documented?
- How does PVT information enter a nodal-analysis workflow?
- Where can I find the relevant Whitson documentation?

## Data Sources

Initial sources:

1. Whitson public Wiki
2. Public whitson+ User Manual

Future optional sources:

3. Public whitsonPVT User Manual
4. Public SNAP documentation
5. Other publicly accessible Whitson educational material

Private Whitson documents, customer data, internal reports, credentials,
and confidential company information are explicitly excluded.

## MVP

The MVP will:

- ingest selected public Whitson documentation
- clean and normalize the documents
- split documents into retrievable chunks
- generate embeddings
- retrieve relevant context
- generate grounded answers with an LLM
- show source citations
- provide an "I don't know" response when evidence is insufficient
- provide a simple user interface
- record basic feedback and evaluation results

## Out of Scope

The MVP will not:

- use confidential Whitson data
- provide project-specific engineering recommendations
- replace engineering judgment
- execute production calculations
- modify Whitson projects
- access private Whitson systems
- claim to be an official Whitson product

## Evaluation

The system will be evaluated using a manually created question
and ground-truth dataset.

Evaluation will include:

- retrieval quality
- source relevance
- answer correctness
- groundedness
- citation quality
- "I don't know" behavior

Different retrieval approaches will be compared where time permits.

## Security and Data Boundaries

Only publicly accessible source material will be used.

No private Whitson files will be copied into this project.

API keys and credentials must never be committed to Git.

Secrets will be provided through environment variables.

## Success Criteria

The project is successful if:

1. A user can ask a technical question.
2. The system retrieves relevant Whitson documentation.
3. The answer is grounded in retrieved evidence.
4. Sources are shown to the user.
5. The system can refuse unsupported questions.
6. Retrieval and answer quality are measured.
7. Another developer can reproduce the project.
8. The application can run independently of the developer's Mac.
