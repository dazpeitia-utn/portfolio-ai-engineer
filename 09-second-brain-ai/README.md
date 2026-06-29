# 🧠 Second Brain AI: Knowledge Graph Builder

Aplicación de gestión de conocimiento y visualización semántica que transforma texto plano y anotaciones en un gráfico de red interactivo estructurando entidades y relaciones jerárquicas.

## 🛠️ Tecnologías Utilizadas
* **Streamlit**: Layout de doble columna para visualización de logs de relaciones y contenedores de gráficos.
* **LangChain**: Formateo estructurado orientado a la generación estricta de payloads JSON sin redundancia de texto.
* **Groq (Meta LLaMA 3.3 70B)**: Procesamiento analítico avanzado (`llama-3.3-70b-versatile`) a baja temperatura para parsing relacional determinista.
* **NetworkX & Matplotlib**: Motor matemático de teoría de grafos y dibujado elástico (`spring_layout`) de redes de información.

## 🚀 Ejecución
Activá tu entorno unificado y lanzá la app:
```bash
cd ..
source venv/bin/activate
cd 09-second-brain-ai
streamlit run app.py