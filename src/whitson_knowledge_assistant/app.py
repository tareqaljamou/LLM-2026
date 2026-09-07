import streamlit as st

from whitson_knowledge_assistant.answer import answer_question


st.set_page_config(
    page_title="Whitson AI Knowledge Navigator",
    page_icon="⛽",
    layout="wide",
)

st.title("Whitson AI Knowledge Navigator")
st.write(
    "A citation-first assistant for public Whitson petroleum-engineering "
    "knowledge."
)

st.info(
    "This prototype uses public indexed sources only. "
    "It does not use private Whitson documents or customer data."
)

question = st.text_input(
    "Ask a petroleum-engineering question",
    placeholder="For example: What is nodal analysis?",
)

if question:
    with st.spinner("Searching public Whitson sources..."):
        try:
            answer = answer_question(question)
            st.markdown(answer)
        except Exception as error:
            st.error(f"An error occurred: {error}")
