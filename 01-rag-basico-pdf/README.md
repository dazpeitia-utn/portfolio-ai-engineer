# 📂 Proyecto 01: Chat con tu PDF (RAG Arquitectura Básica)

Este proyecto consiste en una aplicación web interactiva desarrollada con **Streamlit** que permite a los usuarios cargar documentos PDF y realizar preguntas en lenguaje natural sobre su contenido. La aplicación utiliza una arquitectura **RAG (Retrieval-Augmented Generation)** para responder basándose exclusivamente en el contexto del documento proporcionado.

## 🧠 Conceptos de IA Aplicados
* **RAG (Retrieval-Augmented Generation):** Técnica que optimiza la salida de un Modelo de Lenguaje (LLM) consultando una base de conocimientos externa antes de generar la respuesta.
* **Document Chunking:** Fragmentación de textos largos en bloques significativos utilizando `RecursiveCharacterTextSplitter` para no exceder la ventana de contexto del modelo.
* **Embeddings:** Conversión de texto en vectores numéricos de alta dimensionalidad para capturar el significado semántico.
* **Vector Stores:** Almacenamiento e indexación eficiente de vectores utilizando una base de datos vectorial local (`Chroma`).
* **Semantic Search:** Recuperación de los $k$ fragmentos de texto más relevantes mediante similitud del coseno o distancia vectorial para construir el prompt final.

## 🛠️ Tecnologías y Librerías Utilizadas
* **LangChain:** Framework principal para la orquestación de los componentes de IA y cadenas de ejecución (Chains).
* **Streamlit:** Desarrollo rápido de la interfaz de usuario web nativa en Python.
* **ChatGroq (LLM):** Inferencia en la nube ultra veloz utilizando el modelo de código abierto `llama-3.1-8b-instant`.
* **HuggingFace Embeddings:** Modelo local y gratuito `all-MiniLM-L6-v2` ejecutado en CPU para la vectorización de datos sin costo de API.
* **ChromaDB:** Base de datos vectorial empotrada para el almacenamiento de los vectores.
* **PyPDF:** Extracción de texto y parseo de archivos PDF.

## 🚀 Instrucciones de Ejecución

1. Asegúrate de tener las variables de entorno configuradas en tu archivo `.env`:
   ```env
   GROQ_API_KEY=tu_gsk_api_key_aqui
       
Instala las dependencias del proyecto:
    
    pip install -r requirements.txt

Ejecuta la aplicación de Streamlit:
    
    streamlit run app.py