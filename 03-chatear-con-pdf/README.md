# Proyecto 3: Chatear con tu PDF (Sistema RAG)

Aplicación interactiva construida con **Streamlit** y **LangChain** que permite a los usuarios subir documentos PDF complejos y realizar consultas en lenguaje natural sobre su contenido utilizando una arquitectura RAG (Generación Aumentada por Recuperación).

## 🛠️ Tecnologías utilizadas
- **LLM:** Groq (Llama 3.1 8B)
- **Orquestador:** LangChain
- **Procesamiento de PDF:** PyPDF
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2` local en memoria)
- **Vector Store:** ChromaDB (Base de datos vectorial embebida)
- **Interfaz:** Streamlit

## 🚀 Cómo ejecutar

1. **Clona el proyecto y muévete a la carpeta:**
```
   cd 03-chatear-con-pdf
```

2. **Crea y activa tu entorno virtual:**

```
   python3 -m venv venv
   source venv/bin/activate
```

3. **Instala las dependencias requeridas:**

```
   pip install -r requirements.txt
```

4. **Configura tus variables de entorno:**
Crea un archivo `.env` en la raíz de esta carpeta y añade tu clave de API:

```env
   GROQ_API_KEY=tu_groq_api_key_aqui
```

5. **Corre la aplicación:**

```
   streamlit run app.py
```

## ⚠️ Nota de solución de problemas (macOS / Python 3.9+)

Si experimentas el error `Numpy is not available` o advertencias de inicialización con PyTorch al procesar el PDF, asegúrate de forzar la versión compatible de NumPy corriendo:

```bash
pip install "numpy<2.0.0"
```