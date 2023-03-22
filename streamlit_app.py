import os
import openai
import streamlit as st
import spacy
import tempfile
from docx import Document
from docx.shared import Pt

# Configura tu API key de OpenAI
openai.api_key = "tu_api_key"

# Carga el modelo de lenguaje de spaCy
nlp = spacy.load("en_core_web_sm")

def correct_document(doc):
    corrected_doc = Document()
    for paragraph in doc.paragraphs:
        corrected_paragraph = correct_text(paragraph.text)
        corrected_doc.add_paragraph(corrected_paragraph)
    return corrected_doc

def correct_text(text):
    prompt = f"Please correct the following text for grammar and style: {text}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    corrected_text = response.choices[0].text.strip()
    return corrected_text

st.title("Corrector de gramática y estilo de documentos")

uploaded_file = st.file_uploader("Sube un archivo .docx", type="docx")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
        temp_docx.write(uploaded_file.getvalue())
        doc = Document(temp_docx.name)

    corrected_doc = correct_document(doc)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as corrected_temp_docx:
        corrected_doc.save(corrected_temp_docx.name)
        st.download_button(
            label="Descargar documento corregido",
            data=corrected_temp_docx,
            file_name="documento_corregido.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
