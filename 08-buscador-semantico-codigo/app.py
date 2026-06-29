import streamlit as st
import os
from dotenv import load_dotenv

# Componentes de LangChain especializados en código
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# 1. Configuración de Entorno
load_dotenv()
st.set_page_config(page_title="Code Semantic Search", page_icon="💻", layout="wide")

st.title("💻 Buscador Semántico de Código Fuente")
st.write("Subí archivos de código fuente (Python, JS, etc.) y buscalos conceptualmente por su funcionalidad.")


# 2. Inicialización de Embeddings Locales
@st.cache_resource
def iniciar_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


embeddings_model = iniciar_embeddings()

# 3. Interfaz de carga (Múltiples archivos permitidos)
uploaded_files = st.sidebar.file_uploader(
    "📂 Subí tus archivos de código",
    type=["py", "js", "html", "css", "json"],
    accept_multiple_files=True
)

if uploaded_files:
    st.sidebar.success(f"{len(uploaded_files)} archivos cargados.")

    if st.sidebar.button("⚙️ Indexar Estructura de Código"):
        with st.spinner("Analizando sintaxis e indexando funciones semánticamente..."):
            try:
                documentos = []

                # Configuración del splitter inteligente para lenguaje Python por defecto
                # (Se adapta automáticamente a la sintaxis de funciones, clases y bloques)
                code_splitter = RecursiveCharacterTextSplitter.from_language(
                    language=Language.PYTHON,
                    chunk_size=600,
                    chunk_overlap=100
                )

                for file in uploaded_files:
                    contenido_codigo = file.read().decode("utf-8")

                    # Envolvemos el texto crudo en un documento LangChain inyectando metadatos del archivo
                    doc = Document(
                        page_content=contenido_codigo,
                        metadata={"filename": file.name}
                    )

                    # Splitteamos el código respetando sangrías y definiciones
                    chunks_codigo = code_splitter.split_documents([doc])
                    documentos.extend(chunks_codigo)

                # Construimos el índice vectorial local usando FAISS
                db_codigo = FAISS.from_documents(documentos, embeddings_model)

                # Guardamos la base en sesión para habilitar las búsquedas directas
                st.session_state.db_codigo = db_codigo
                st.session_state.codigo_listo = True
                st.sidebar.success(f"¡Listo! {len(documentos)} bloques de código indexados.")

            except Exception as e:
                st.sidebar.error(f"Error procesando los archivos: {e}")

# 4. Motor de Búsqueda Semántica
if "codigo_listo" in st.session_state and st.session_state.codigo_listo:
    st.subheader("🔍 ¿Qué funcionalidad estás buscando?")
    query_busqueda = st.text_input(
        "Escribí en lenguaje natural qué hace la función (Ej: 'Carga de archivos pdf', 'Configuración del LLM de groq'):"
    )

    if query_busqueda:
        db = st.session_state.db_codigo
        # Buscamos los 3 bloques de código más cercanos conceptualmente
        resultados = db.similarity_search(query_busqueda, k=3)

        st.markdown(f"### 🎯 Fragmentos de código más relevantes:")

        for i, doc in enumerate(resultados):
            nombre_archivo = doc.metadata.get("filename", "Desconocido")
            st.markdown(f"#### 📄 Resultado {i + 1} - Archivo: `{nombre_archivo}`")

            # Mostramos el bloque de código formateado limpiamente dentro de markdown
            st.code(doc.page_content, language="python")
            st.markdown("---")
else:
    st.info("💡 Subí uno o más scripts de código en la barra lateral e indexalos para habilitar la búsqueda semántica.")