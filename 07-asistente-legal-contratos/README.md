# ⚖️ AI Legal Contract Auditor

Sistema automatizado de auditoría y análisis de riesgo contractual diseñado para procesar acuerdos comerciales extensos, identificar cláusulas leoninas o abusivas y resumir obligaciones corporativas.

## 🛠️ Tecnologías Utilizadas
* **Streamlit**: Dashboard fluido para presentación de matrices de riesgo.
* **LangChain**: Tubería de transformación y paso de prompts estructurados (`ChatPromptTemplate`).
* **PyPDFLoader**: Extracción nativa de texto estructurado de contratos en PDF.
* **Groq (Meta LLaMA 3.3 70B)**: Uso del modelo `llama-3.3-70b-versatile` configurado con temperatura baja (`0.1`) para garantizar máxima precisión semántica y evitar alucinaciones en interpretaciones de leyes o contratos.

## 🚀 Cómo Ejecutarlo
Recordá activar el entorno virtual global desde la raíz antes de lanzar la app:
```bash
cd ..
source venv/bin/activate
cd 07-asistente-legal-contratos
streamlit run app.py