import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# 1. Cargar variables de entorno (API Key de Groq)
load_dotenv()

st.title("📂 Chat con tu PDF (RAG con Groq - 100% Gratis)")
st.write("Sube un documento y hazle preguntas específicas.")

uploaded_file = st.file_uploader("Elige un archivo PDF", type="pdf")

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("¡Archivo subido con éxito! Procesando...")

    # 2. Procesamiento del documento
    loader = PyPDFLoader("temp.pdf")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 3. Embeddings Gratuitos de HuggingFace (No necesitas API Key para esto)
    # Nota: La primera vez puede tardar un poquito en descargar el modelo de embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 4. Configurar el LLM de Groq (Usamos llama3-8b que es excelente y gratis)
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

    system_prompt = (
        "Eres un asistente experto en análisis de documentos.\n"
        "Responde la pregunta del usuario utilizando únicamente el siguiente contexto recuperado. "
        "Si no sabes la respuesta o no está en el contexto, di que no la encuentras, no inventes nada.\n\n"
        "Contexto:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # 5. Crear la cadena de ejecución (Chain)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # 6. Interfaz de usuario para la pregunta
    user_question = st.text_input("¿Qué quieres saber sobre este documento?")

    if user_question:
        with st.spinner("Pensando con Groq..."):
            response = rag_chain.invoke({"input": user_question})

            st.subheader("Respuesta:")
            st.write(response["answer"])

            if os.path.exists("temp.pdf"):
                os.remove("temp.pdf")