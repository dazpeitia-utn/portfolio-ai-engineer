# Proyecto 5: Agente Investigador Web Autónomo (AI Agent with Tool Use)

Aplicación que implementa un **Agente de IA Autónomo** capaz de razonar, planificar y ejecutar herramientas externas (búsqueda web en tiempo real) para resolver investigaciones complejas sobre cualquier tópico solicitado por el usuario.

## 🛠️ Tecnologías utilizadas
- **LLM Engine:** Groq (`qwen/qwen3.6-27b`)
- **Orquestador de Agentes:** LangChain Agents (Conversational React)
- **Herramientas (Tools):** DuckDuckGo Search API (Navegación web en tiempo real)
- **Interfaz:** Streamlit con soporte de descarga de reportes (.md)

## 🚀 Cómo ejecutar
1. Activa el entorno: `source venv/bin/activate`
2. Instala las dependencias: `pip install -r requirements.txt`
3. Configura tu `GROQ_API_KEY` en el `.env`
4. Corre la app: `streamlit run app.py`