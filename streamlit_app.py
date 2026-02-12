import streamlit as st
from settings import Settings
from rag_pipeline import SimpleRAG

st.set_page_config(page_title="Enkel RAG", page_icon="🔎", layout="centered")
st.title("Enkel RAG-bot")
st.caption("Enkel fråga → webbsök → embeddings → kort svar.")

prompt = st.text_input("Vad vill du veta?", placeholder="Skriv din fråga här...")

if prompt:
    try:
        with st.spinner("Hämtar och sammanfattar..."):
            rag = SimpleRAG(Settings())
            answer = rag.run(prompt)
        st.success("Svar")
        st.write(answer)
    except Exception as e:
        st.error("Något gick fel. Kontrollera nycklar, Qdrant och nät.")
        st.caption(str(e))
else:
    st.info("Ange en fråga för att hämta ett svar.")
