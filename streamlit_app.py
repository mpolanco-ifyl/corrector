import os
import openai
import streamlit as st
import docx
from docx import Document
from io import BytesIO

# Configura tu clave API de OpenAI
openai.api_key = "tu_clave_api"

# Función para procesar el texto con GPT-4 y corregir la gramática y el estilo
def corregir_texto(texto):
    prompt = f"Corrija la gramática y el estilo del siguiente texto:\n\n{texto}\n\nTexto corregido:"
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    texto_corregido = completions.choices[0].text.strip()
    return texto_corregido

# Función para corregir un documento docx
def corregir_docx(documento):
    doc = Document(documento)
    for paragraph in doc.paragraphs:
        texto_original = paragraph.text
        texto_corregido = corregir_texto(texto_original)
        paragraph.text = texto_corregido

    output_doc = BytesIO()
    doc.save(output_doc)
    output_doc.seek(0)
    return output_doc

# Interfaz de Streamlit
st.set_page_config(page_title="Corrección de gramática y estilo", page_icon=None, layout="wide", initial_sidebar_state="auto")

st.title("Corrección automática de gramática y estilo de documentos")
st.write("Esta aplicación utiliza GPT-4 para corregir automáticamente la gramática y el estilo de tus documentos en formato .docx.")

uploaded_file = st.file_uploader("Sube un archivo .docx", type=["docx"])

if uploaded_file is not None:
    if st.button("Corregir documento"):
        with st.spinner("Corrigiendo gramática y estilo..."):
            corrected_doc = corregir_docx(uploaded_file)
            st.success("Documento corregido con éxito")
            st.download_button(label="Descargar documento corregido", data=corrected_doc, file_name="documento_corregido.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
