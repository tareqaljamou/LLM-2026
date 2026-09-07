from whitson_knowledge_assistant.ingest import clean_text, make_chunks


def test_clean_text_removes_script_content() -> None:
    html = """
    <html>
        <body>
            <h1>Nodal Analysis</h1>
            <p>IPR and VLP describe well performance.</p>
            <script>secret_script_content()</script>
        </body>
    </html>
    """

    text = clean_text(html)

    assert "Nodal Analysis" in text
    assert "IPR and VLP" in text
    assert "secret_script_content" not in text


def test_make_chunks_returns_multiple_chunks() -> None:
    text = "word " * 600

    chunks = make_chunks(text)

    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)
