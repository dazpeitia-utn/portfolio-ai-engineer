import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate

# 1. Inicialización y Seguridad
load_dotenv()
st.set_page_config(page_title="Legal Contract Auditor", page_icon="⚖️", layout="wide")

st.title("⚖️ Asistente Legal: Auditor Inteligente de Contratos")
st.write("Subí cualquier contrato comercial o acuerdo en PDF para extraer cláusulas clave y evaluar niveles de riesgo.")

if not os.getenv("GROQ_API_KEY"):
    st.error("Falta la API Key de Groq. Configurala en tu archivo .env en la raíz del proyecto.")
    st.stop()


# Reutilizamos el entorno centralizado consumiendo el LLM potente de Groq
@st.cache_resource
def iniciar_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)


llm = iniciar_llm()
TEMP_LEGAL_PDF = "temp_contrato.pdf"

# 2. Interfaz Lateral
uploaded_contract = st.sidebar.file_uploader("📂 Cargar Contrato (PDF)", type=["pdf"])

if uploaded_contract:
    st.sidebar.success("Contrato cargado con éxito.")

    with open(TEMP_LEGAL_PDF, "wb") as f:
        f.write(uploaded_contract.getbuffer())

    if st.sidebar.button("🔍 Auditar Contrato Ahora"):
        with st.spinner("Analizando estructura legal, buscando penalizaciones y evaluando riesgos comerciales..."):
            try:
                # Extracción completa de texto del contrato
                loader = PyPDFLoader(TEMP_LEGAL_PDF)
                paginas = loader.load()
                texto_completo = "\n".join([pag.page_content for pag in paginas])

                # Prompt de Ingeniería Legal Avanzada
                prompt_legal = ChatPromptTemplate.from_messages([
                    ("system", (
                        "Sos un consultor legal corporativo y abogado experto en auditoría de contratos comerciales.\n"
                        "Tu tarea es analizar exhaustivamente el contrato provisto por el usuario y generar un informe "
                        "estructurado riguroso en formato Markdown.\n\n"
                        "Debes estructurar tu respuesta EXACTAMENTE en las siguientes secciones:\n"
                        "1. **Resumen Ejecutivo**: Breve explicación de qué trata el acuerdo y quiénes son las partes firmantes.\n"
                        "2. **Obligaciones Críticas**: Lista detallada de los entregables y compromisos principales de cada parte.\n"
                        "3. **Matriz de Análisis de Riesgo**: Una tabla en Markdown con las columnas [Cláusula / Tema | Nivel de Riesgo (Bajo/Medio/Alto) | Impacto / Recomendación]. Analizá puntos críticos como renovación automática, penalizaciones por incumplimiento, rescisión anticipada y jurisdicción aplicable.\n"
                        "4. **Fechas Clave y Plazos**: Listado con viñetas de todas las fechas límite, vigencias o prórrogas encontradas.\n\n"
                        "Si el documento no especifica algún punto, indicalo explícitamente como 'No mencionado en el documento' para evitar alucinaciones."
                    )),
                    ("human", "Aquí está el texto completo del contrato para auditar:\n\n{contrato_texto}")
                ])

                # Cadena directa (Inyección de documento completo para análisis holístico)
                chain = prompt_legal | llm
                respuesta_auditoria = chain.invoke({"contrato_texto": texto_completo})

                # Guardamos el reporte en el estado de la sesión para evitar que se borre si interactúan con la UI
                st.session_state.reporte_legal = respuesta_auditoria.content

                if os.path.exists(TEMP_LEGAL_PDF):
                    os.remove(TEMP_LEGAL_PDF)

            except Exception as e:
                st.error(f"Error durante el análisis del contrato: {e}")

# 3. Renderizado de Resultados
if "reporte_legal" in st.session_state:
    st.subheader("📋 Informe de Auditoría de Riesgos")
    st.markdown(st.session_state.reporte_legal)
else:
    st.info(
        "💡 Por favor, cargá un contrato en formato PDF en el panel de la izquierda y presioná 'Auditar Contrato Ahora' para procesarlo.")