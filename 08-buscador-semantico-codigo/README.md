# 💻 Code Semantic Search

Motor de búsqueda conceptual y semántica para repositorios de código fuente, utilizando división sintáctica por lenguajes y almacenamiento vectorial local en memoria.

## 🛠️ Tecnologías Utilizadas
* **Streamlit**: Interfaz web intuitiva para ingreso de queries y renderizado de bloques de código formateados.
* **LangChain Text Splitters**: Uso de `RecursiveCharacterTextSplitter.from_language` para respetar estructuras de programación (`def`, `class`, scopes) evitando cortes destructivos.
* **HuggingFace Embeddings**: Vectorización local a costo cero.
* **FAISS (Facebook AI Similarity Search)**: Motor vectorial en memoria de alto rendimiento para cálculos inmediatos de distancia coseno en tensores de código.

## 🚀 Ejecución
Activá tu entorno unificado y lanzá la app:
```bash
cd ..
source venv/bin/activate
cd 08-buscador-semantico-codigo
streamlit run app.py