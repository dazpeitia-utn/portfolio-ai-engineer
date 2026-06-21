import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# 1. Cargar variables de entorno (.env)
load_dotenv()

st.set_page_config(page_title="Agente de IA con Herramientas", page_icon="🤖")
st.title("🤖 Agente de Investigación con Herramientas")
st.write("Este agente puede razonar, buscar en internet en tiempo real y resolver matemáticas complejas de forma autónoma.")

# Verificar que la API Key esté presente
if not os.getenv("GROQ_API_KEY"):
    st.error("Por favor, configura tu GROQ_API_KEY en el archivo .env de esta carpeta.")
    st.stop()

# 2. Configurar el cerebro del Agente (LLM de Groq)
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# 3. Definir las herramientas (Tools) que el agente puede manipular
search = DuckDuckGoSearchRun()

def calculadora(expresion: str) -> str:
    try:
        # Evalúa de forma segura operaciones matemáticas básicas en Python
        return str(eval(expresion, {"__builtins__": None}, {}))
    except Exception:
        return "Error al calcular la expresión numérica."

tools = [
    Tool(
        name="Busqueda_Web",
        func=search.run,
        description="Útil para cuando necesitas responder preguntas sobre eventos actuales, noticias, fechas o datos que requieren buscar en internet en tiempo real. Modifica los términos de búsqueda si no encuentras lo que buscas."
    ),
    Tool(
        name="Calculadora",
        func=calculadora,
        description="Útil para resolver operaciones matemáticas. Ingresa únicamente expresiones numéricas directas como (2026-1948) o 45000/3."
    )
]

# 4. Diseñar el Prompt del Agente (Con instrucciones anti-bucles)
template = """Eres un asistente de investigación de IA altamente analítico y metódico. Pensarás y responderás siempre en español.
Tienes acceso a las siguientes herramientas:

{tools}

Para responder a la pregunta del usuario, DEBES seguir estrictamente este formato exacto paso a paso. No agregues ninguna palabra extra a los prefijos:

Thought: Siempre debes pensar qué hacer a continuación en español. ¿Necesito usar una herramienta? Sí o No.
Action: El nombre exacto de la herramienta a usar, debe ser obligatoriamente una de estas: [{tool_names}]. No agregues texto explicativo aquí, solo escribe el nombre.
Action Input: El parámetro o consulta exacta para la herramienta. No repitas la misma consulta exacta más de dos veces si los resultados no te sirven. Cambia los términos de búsqueda.
Observation: El resultado que devuelve la herramienta.

(Este proceso de Thought/Action/Action Input/Observation se puede repetir si es necesario)

Si tras buscar no encuentras la información exacta en los resultados web pero tú conoces la respuesta gracias a tu propio conocimiento previo, detén las búsquedas y formula tu respuesta final.

Thought: Ya recopilé toda la información necesaria o usaré mi conocimiento para dar la respuesta final.
Final Answer: La respuesta detallada, precisa y explicada completamente en español para el usuario.

Pregunta del usuario: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# 5. Construir el orquestador del Agente (Agent Executor con límites estrictos)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,  # Evita por completo que corra infinitamente si se traba
    early_stopping_method="generate", # Si llega al límite de iteraciones, genera una respuesta con lo que tenga
    handle_parsing_errors="Check your output format. Remember to use exact tool names from [Busqueda_Web, Calculadora] and do not add extra text in Action prefix."
)

# 6. Interfaz gráfica con Streamlit
user_query = st.text_input("¿Qué deseas que investigue hoy?", placeholder="Ej: ¿Cuántos años pasaron desde la fundación de la UTN hasta hoy?")

if user_query:
    with st.spinner("El agente está ejecutando su bucle de razonamiento..."):
        try:
            response = agent_executor.invoke({"input": user_query})
            st.subheader("💡 Respuesta Final del Agente:")
            st.write(response["output"])
        except Exception as e:
            st.error(f"Ocurrió un error en el agente: {e}")