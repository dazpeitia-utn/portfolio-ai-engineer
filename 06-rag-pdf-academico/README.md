# 🎓 Academic PDF RAG Analyzer

Sistema de Recuperación Aumentada por Generación (RAG) diseñado para el análisis profundo de papers científicos, artículos académicos y reportes técnicos extensos con procesamiento local de embeddings.

## 🛠️ Tecnologías Utilizadas
* **Streamlit**: Interfaz de usuario interactiva y fluida.
* **LangChain**: Estructura de orquestación (`create_retrieval_chain` y `create_stuff_documents_chain`).
* **ChromaDB**: Base de datos vectorial local y persistente en disco.
* **HuggingFace Embeddings & PyTorch**: Vectorización local a través del modelo nativo `sentence-transformers/all-MiniLM-L6-v2`.
* **Groq (Meta LLaMA 3.3 70B)**: Procesamiento y razonamiento lógico-académico ultra veloz con el modelo de producción de última generación `llama-3.3-70b-versatile`.

## 📦 Gestión del Entorno Virtual (Monorepositorio)
Para optimizar el espacio en disco de la máquina y evitar redundancias, este proyecto **no cuenta con un entorno virtual propio**, sino que consume y comparte de forma eficiente el entorno centralizado localizado en la **raíz del portfolio**:

```bash
# 1. Pararse en la raíz del portfolio principal
cd /Users/jorgediegodanielazpeitia/Desktop/Proyectos/Python/portfolio-ai-engineer

# 2. Activar el entorno virtual unificado
source venv/bin/activate

# 3. Moverse a la carpeta de este proyecto
cd 06-rag-pdf-academico

# 4. Ejecutar la aplicación
streamlit run app.py