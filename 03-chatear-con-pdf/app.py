import streamlit as st
import os
from dotenv import load_dotenv
from pypdf import PdfReader

# Componentes de LangChain
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Cargar variables de entorno
load_dotenv()

st.set_page_config(page_title="Pregúntale a tu PDF", page_icon="📄", layout="wide")
st.title("📄 Chatea con tus Documentos (Sistema RAG)")
st.write("Sube un archivo PDF y la IA te responderá basándose **únicamente** en su contenido.")

if not os.getenv("GROQ_API_KEY"):
    st.error("Por favor, configura tu GROQ_API_KEY en el archivo .env")
    st.stop()

# Inicializar el modelo de Groq
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

# 2. Configurar la barra lateral para subir archivos
with st.sidebar:
    st.header("📥 Cargar Documento")
    uploaded_file = st.file_uploader("Sube tu archivo PDF aquí", type=["pdf"])

# Mantener la base de datos vectorial en la sesión de Streamlit para no recrearla en cada clic
if uploaded_file is not None:
    if "vector_store" not in st.session_state:
        with st.spinner("Procesando y analizando el PDF... Esto puede demorar un momento."):
            try:
                # A. Extraer texto del PDF
                reader = PdfReader(uploaded_file)
                raw_text = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        raw_text += text

                # B. Fragmentar el texto (Chunking)
                # Rompemos el documento en bloques de 1000 caracteres con un solapamiento de 200
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = text_splitter.split_text(raw_text)

                # C. Crear Embeddings (Convertir texto a vectores matemáticos)
                # Usamos un modelo liviano de HuggingFace que corre gratis en tu Mac
                embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

                # D. Guardar fragmentos en ChromaDB (Base de datos vectorial temporal)
                vector_store = Chroma.from_texts(chunks, embeddings)
                st.session_state.vector_store = vector_store
                st.sidebar.success("✅ ¡PDF indexado con éxito!")
            except Exception as e:
                st.sidebar.error(f"Error al procesar el archivo: {e}")
                st.stop()

    # 3. Flujo de Chat (Interfaz de usuario)
    st.subheader("💬 Hazle preguntas al documento")
    user_question = st.text_input("¿Qué deseas saber sobre este PDF?")

    if user_question:
        with st.spinner("Buscando en el documento y redactando respuesta..."):
            # Configurar el recuperador (Retriever) para buscar los 3 fragmentos más similares
            retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})

            # Diseñar el prompt del sistema
            system_prompt = (
                "Eres un asistente experto encargado de responder preguntas utilizando "
                "estrictamente el contexto provisto a continuación. Si no sabes la respuesta "
                "o no se encuentra en el texto, di claramente que la información no está en el documento. "
                "Mantén las respuestas claras, concisas y en español.\n\n"
                "Contexto:\n{context}"
            )

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])

            # Crear las cadenas de ejecución de LangChain (Retrieval Chain)
            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)

            # Ejecutar la consulta
            response = rag_chain.invoke({"input": user_question})

            # Mostrar la respuesta final
            st.write(response["answer"])

            # Mostrar las fuentes de donde sacó la información (Opcional, muy profesional)
            with st.expander("🔍 Ver fragmentos del documento utilizados como fuente"):
                for i, doc in enumerate(response["context"]):
                    st.markdown(f"**Fragmento {i + i}:**")
                    st.caption(doc.page_content)
else:
    st.info("👋 Por favor, sube un archivo PDF en la barra lateral para comenzar a chatear.")