import streamlit as st
import os
import requests
import time  # <--- Importante para manejar los delays anti-bloqueo
from dotenv import load_dotenv

# Componentes modernos de LangChain
from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. Cargar variables de entorno
load_dotenv()

st.set_page_config(page_title="AI Trend Scout Agent", page_icon="🕵️‍♂️", layout="wide")
st.title("🕵️‍♂️ Agente Investigador Web Autónomo")
st.write("Escribe cualquier tópico y el agente navegará en tiempo real para armarte un reporte con datos frescos.")

if not os.getenv("GROQ_API_KEY"):
    st.error("Por favor, configura tu GROQ_API_KEY en el archivo .env")
    st.stop()


# 2. FUNCIÓN DE BÚSQUEDA OPTIMIZADA (Con manejo de Rate Limits)
def buscar_en_duckduckgo(query: str) -> str:
    try:
        # Añadimos un pequeño delay de cortesía para evitar baneos de IP por peticiones ráfaga
        time.sleep(1)

        # Usamos la API HTML de DuckDuckGo que es más permisiva con TLS viejos
        url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.post(url, data={"q": query}, headers=headers, timeout=10)

        if response.status_code == 200:
            # Extraemos texto plano básico de los primeros resultados para el agente
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            resultados = []
            for i, result in enumerate(soup.find_all("a", class_="result__snippet")):
                if i < 4:
                    resultados.append(result.get_text(strip=True))
            return "\n\n".join(
                resultados) if resultados else "No se encontraron resultados específicos en la web para esta consulta."

        return "Error al conectar con el motor de búsqueda (Posible bloqueo temporal por exceso de peticiones)."
    except Exception as e:
        return f"Error en la búsqueda web: {str(e)}"


# Configuramos la herramienta usando nuestra función segura
search_tool = Tool(
    name="duckduckgo_search",
    description="Obligatorio para buscar resultados de partidos, noticias de hoy, goles y eventos en tiempo real.",
    func=buscar_en_duckduckgo,
)
tools = [search_tool]

# 3. Inicializar el LLM con soporte nativo de herramientas
llm = ChatGroq(model="qwen/qwen3.6-27b", temperature=0.1)

# Prompt del sistema moderno para el Agente de Tool Calling
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un agente de investigación profesional de última generación. "
     "CONTEXTO TEMPORAL CRUCIAL: El año actual es 2026. Hoy es exactamente lunes 22 de junio de 2026 y la Copa del Mundo de la FIFA 2026 se está jugando en este preciso momento en Norteamérica. "
     "Tu objetivo es buscar en internet usando 'duckduckgo_search' para obtener las crónicas, goles y marcadores reales de los partidos que ya se jugaron (como los de ayer, domingo 21 de junio de 2026). "
     "Bajo ninguna circunstancia digas que el mundial 'no ha comenzado' o que 'se celebrará en el futuro'. Confía ciegamente en los resultados que te traiga la herramienta de búsqueda actual. "
     "MUY IMPORTANTE: Si realizas una búsqueda y los resultados son ambiguos, publicitarios, o el motor de búsqueda te da error, NO sigas buscando obsesivamente cambiando los términos de la consulta. Formula tu respuesta final basándote en que no se pudo recuperar la información en ese instante o con lo poco que tengas disponible. Evita bucles innecesarios. "
     "Responde de forma estructurada y con buen formato Markdown."),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Crear el agente moderno con salvaguardas contra bucles infinitos
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5  # <--- LIMITADOR DE ITERACIONES: Detiene al agente tras 5 intentos para cuidar tu API Key
)

# 4. Interfaz de usuario
topic_input = st.text_input(
    "📝 ¿Qué deseas investigar hoy?",
    placeholder="Ej: Resultados y goles de los partidos del mundial del 21/6/2026..."
)

if "respuesta_agente" not in st.session_state:
    st.session_state.respuesta_agente = None

if topic_input:
    if st.button("🚀 Iniciar Investigación en Tiempo Real"):
        with st.spinner("El Agente está buscando activamente en la web..."):
            try:
                resultado = agent_executor.invoke({
                    "input": topic_input,
                    "chat_history": []
                })
                st.session_state.respuesta_agente = resultado["output"]
            except Exception as e:
                st.error(f"Hubo un problema durante la investigación del agente: {e}")

if st.session_state.respuesta_agente:
    st.success("¡Investigación completada!")
    st.subheader("📋 Reporte en Tiempo Real Generado")
    st.markdown(st.session_state.respuesta_agente)

    st.download_button(
        label="📥 Descargar Reporte (.md)",
        data=st.session_state.respuesta_agente,
        file_name="reporte_mundial.md",
        mime="text/markdown"
    )