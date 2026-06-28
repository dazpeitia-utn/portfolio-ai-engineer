# 📓 Notas de Ingeniería & Aprendizajes: Proyecto 06

## 🎯 El Desafío Técnico
El objetivo de este proyecto fue evolucionar los sistemas RAG básicos en memoria (Proyectos 01 y 03) hacia una arquitectura persistente, local y optimizada para el procesamiento de documentos densos (papers científicos y reportes de investigación) sin disparar los costos de APIs externas y garantizando máxima robustez lógica ante consultas complejas.

## 🧱 Decisiones de Arquitectura & Por qué las tomé

### 1. Vectorización 100% Local con HuggingFace (`all-MiniLM-L6-v2`)
*   **Decisión:** En lugar de delegar el cálculo de embeddings a una API paga (como OpenAI), integré el modelo local de `sentence-transformers` corriendo directamente en los recursos de mi máquina.
*   **Impacto:** Logré costo cero en la etapa de vectorización e indexación de documentos, eliminando la latencia de red y garantizando privacidad absoluta de los datos del paper antes de enviarle el contexto refinado al LLM.

### 2. Base de Datos Vectorial Persistente con ChromaDB
*   **Decisión:** Implementé un almacenamiento físico en disco (`persist_directory="chroma_db"`).
*   **Impacto:** Adiós al procesamiento volátil en memoria. Al persistir el índice vectorial, la aplicación no necesita re-indexar ni volver a procesar el PDF si el usuario recarga la interfaz o regresa al día siguiente. El conocimiento queda consolidado en storage.

### 3. Estrategia de Chunking Avanzado (Recursive + Overlap)
*   **Decisión:** Configuré un `RecursiveCharacterTextSplitter` con un `chunk_size` de 1000 caracteres y un `chunk_overlap` de 200.
*   **Impacto:** Los textos académicos tienen una densidad de hipótesis, fórmulas y metodologías muy alta. El solapamiento (overlap) de 200 caracteres actúa como un buffer de contexto que evita que las ideas o argumentos científicos se corten a la mitad entre un vector y otro, incrementando drásticamente la precisión del recuperador (`retriever`).

### 4. Trazabilidad y Auditoría mediante Metadatos
*   **Decisión:** Diseñé la tubería de extracción para inyectar el número de página de origen en las respuestas mediante la extracción de metadatos del objeto `Document`.
*   **Impacto:** Clave para mitigar alucinaciones en entornos científicos. El usuario puede auditar el fragmento exacto y la página del paper original que alimentó el prompt del LLM.

### 5. Actualización Crítica del Modelo de Razonamiento (Groq API)
*   **Decisión:** Se migró la orquestación del LLM del modelo obsoleto `llama3-8b-8192` al nuevo estándar activo de la API de Groq: `llama-3.3-70b-versatile`.
*   **Impacto:** Se evitó el quiebre de la aplicación por desuso de modelos deprecados y se ganó una capacidad masiva de razonamiento matemático y lógico (70B parámetros), ideal para desmenuzar papers complejos como "Attention Is All You Need".

## 💡 Conceptos Clave Aprendidos / Reforzados

### 💥 Conflictos de Dependencias Nativas (El "Infierno de NumPy 2.0")
*   **Aprendizaje:** Las librerías de IA locales (`torch`, `onnxruntime`) requieren compilaciones de bajo nivel altamente sensibles. Aprendí a diagnosticar errores de inicialización provocados por actualizaciones del mercado (como NumPy 2.0) y a fijar límites seguros en los entornos (`"numpy<2"`) para estabilizar los motores matemáticos del proyecto en macOS.

### 📁 Arquitectura de Entornos en Monorepositorios
*   **Aprendizaje:** Entendí el beneficio de centralizar un único entorno virtual en la raíz de un portafolio de 25 proyectos de Python en lugar de fragmentar un `venv` por cada app. Esto ahorra decenas de gigabytes de disco y agiliza el flujo de trabajo diario aislando las librerías compartidas de IA (`langchain`, `streamlit`, `chromadb`) en un solo motor de ejecución.

### 🛑 Inyección de Contexto Limpio y Anti-Alucinación
*   **Aprendizaje:** Aprendí a diseñar prompts de sistema estrictos donde se limite al LLM a responder *únicamente* si la información reside en los chunks recuperados, forzando la honestidad del modelo ante vacíos de información o preguntas trampa (ej. consultar datos de GPT-4 dentro de un paper de 2017).