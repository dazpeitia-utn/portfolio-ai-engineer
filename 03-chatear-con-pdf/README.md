# Proyecto 3: Chatear con tu PDF (Sistema RAG)

Aplicación interactiva construida con **Streamlit** y **LangChain** que permite a los usuarios subir documentos PDF complejos y realizar consultas en lenguaje natural sobre su contenido.

## 🛠️ Tecnologías utilizadas
- **LLM:** Groq (Llama 3.1 8B)
- **Orquestador:** LangChain
- **Procesamiento de PDF:** PyPDF
- **Embeddings:** HuggingFace (Modelos locales en memoria)
- **Vector Store:** ChromaDB (Base de datos vectorial local)
- **Interfaz:** Streamlit

## 🚀 Cómo ejecutar
1. Asegúrate de tener el entorno virtual activo: `source venv/bin/activate`
2. Configura tu `GROQ_API_KEY` en el archivo `.env`.
3. Corre la aplicación: `streamlit run app.py`