import streamlit as st
import os
import shutil
from dotenv import load_dotenv

# Componentes de LangChain
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# 1. Configuración de entorno y página
load_dotenv()
st.set_page_config(page_title="Academic PDF RAG", page_icon="🎓", layout="wide")

st.title("🎓 Analizador RAG de Papers Académicos")
st.write("Subí tus papers científicos en PDF y chateá con ellos usando embeddings locales y Groq.")

if not os.getenv("GROQ_API_KEY"):
    st.error("Por favor, configura tu GROQ_API_KEY en el archivo .env en la raíz del proyecto.")
    st.stop()

DB_DIR = "chroma_db"
TEMP_PDF = "temp_paper.pdf"


# 2. Inicializar el LLM y los Embeddings (Locales y livianos)
@st.cache_resource
def inicializar_modelos():
    # Modelo local para calcular vectores gratis en tu Mac
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Modelo de producción actualizado y activo en Groq para razonamiento avanzado
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
    return embeddings, llm


embeddings_model, llm_model = inicializar_modelos()

# 3. Interfaz de carga de archivos
uploaded_file = st.sidebar.file_uploader("📂 Subí un paper académico (PDF)", type=["pdf"])

if uploaded_file:
    st.sidebar.success("PDF cargado con éxito.")

    with open(TEMP_PDF, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.sidebar.button("🧠 Indexar y Procesar Documento"):
        with st.spinner("Leyendo PDF, generando chunks y calculando embeddings vectoriales..."):
            try:
                if os.path.exists(DB_DIR):
                    shutil.rmtree(DB_DIR)

                loader = PyPDFLoader(TEMP_PDF)
                paginas = loader.load()

                # Chunking con Overlap optimizado para que no se corten las ideas científicas
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                chunks = text_splitter.split_documents(paginas)

                # Persistencia física en disco mediante ChromaDB
                vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings_model,
                    persist_directory=DB_DIR
                )

                st.session_state.vector_ready = True
                st.sidebar.success(f"¡Listo! Se generaron {len(chunks)} fragmentos indexados.")

                if os.path.exists(TEMP_PDF):
                    os.remove(TEMP_PDF)

            except Exception as e:
                st.sidebar.error(f"Error procesando el PDF: {e}")

# 4. Zona de chat interactivo
if "vector_ready" in st.session_state and st.session_state.vector_ready:
    db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings_model)
    retriever = db.as_retriever(search_kwargs={"k": 4})

    # Prompt estricto anti-alucinaciones científico
    system_prompt = (
        "Sos un asistente de investigación de élite. Tu tarea es responder la consulta del usuario "
        "utilizando únicamente el contexto académico provisto a continuación. Si no sabés la respuesta "
        "o si no está explícitamente en el texto, decí que la información no está disponible en el documento.\n\n"
        "Contexto recuperado:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm_model, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    st.subheader("💬 Hacer preguntas al Paper")
    user_query = st.text_input("Escribí tu pregunta sobre metodología, resultados o conclusiones:")

    if user_query:
        with st.spinner("Buscando en la base vectorial y redactando respuesta..."):
            response = rag_chain.invoke({"input": user_query})

            st.markdown("### 🤖 Respuesta del Asistente")
            st.write(response["answer"])

            st.markdown("---")
            with st.expander("📚 Ver fuentes del documento original (Chunks usados)"):
                for doc in response["context"]:
                    page_num = doc.metadata.get("page", 0) + 1
                    st.markdown(f"**Fragmento de la Página {page_num}:**")
                    st.caption(doc.page_content)
                    st.markdown("---")
else:
    st.info("💡 Por favor, subí un archivo PDF desde la barra lateral e indexalo para comenzar a chatear.")