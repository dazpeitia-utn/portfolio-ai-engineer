import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Configuración de Entorno e Interfaz
load_dotenv()
st.set_page_config(page_title="AI Travel Itinerary Agent", page_icon="✈️", layout="wide")

st.title("✈️ Agente Inteligente de Itinerarios de Viaje")
st.write(
    "Planificá tu próximo viaje ingresando múltiples variables de manera simultánea. La IA optimizará tu ruta, tiempos y presupuesto de forma lógica.")

if not os.getenv("GROQ_API_KEY"):
    st.error("Falta la API Key de Groq. Configurala en tu archivo .env en la raíz del proyecto.")
    st.stop()


@st.cache_resource
def iniciar_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)


llm = iniciar_llm()

# 2. Formulario de Variables Múltiples (UI)
col1, col2 = st.columns(2)

with col1:
    destino = st.text_input("📍 ¿A qué ciudad o país viajás?", placeholder="Ej: Tokio, Japón / Roma, Italia")

    # Reemplazo del Slider por un Calendario de Selección de Rango de Fechas
    fechas = st.date_input(
        "📅 Seleccioná el rango de tu viaje (Ida y Vuelta):",
        value=(datetime.now().date(), datetime.now().date()),  # Inicializa en el día de hoy
        min_value=datetime.now().date()  # Evita que elijan fechas pasadas
    )

    # Lógica de control para calcular los días dinámicamente
    if isinstance(fechas, tuple) and len(fechas) == 2:
        fecha_inicio, fecha_fin = fechas
        # Sumamos 1 para que cuente el día de llegada y salida completo
        dias = (fecha_fin - fecha_inicio).days + 1
        st.info(
            f"⏳ Duración calculada: **{dias} días** ({fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')})")
    else:
        dias = 1
        st.warning("⚠️ Por favor, seleccioná ambas fechas (ida y vuelta) en el calendario.")

    presupuesto = st.number_input("💰 Presupuesto estimado total (USD)", min_value=100, max_value=100000, value=1500,
                                  step=100)

with col2:
    estilo_viaje = st.selectbox(
        "🎒 Estilo de viaje preferido:",
        ["Mochilero / Low-Cost", "Equilibrado (Calidad/Precio)", "Lujo y Confort", "Aventura / Actividades Intensas"]
    )
    restricciones = st.text_area(
        "⚠️ Restricciones o preferencias especiales (Alimentación, movilidad, intereses):",
        placeholder="Ej: Comida vegetariana, viajar con niños pequeños, preferencia por museos de arte o evitar caminatas muy largas."
    )

# 3. Ejecución del Agente Planificador
if st.button("🗺️ Generar Itinerario Optimizado"):
    if not destino.strip():
        st.warning("Por favor, ingresá un destino válido para comenzar la planificación.")
    elif isinstance(fechas, tuple) and len(fechas) < 2:
        st.error("No se puede generar el itinerario sin definir una fecha de regreso.")
    else:
        with st.spinner(
                f"El Agente de Viajes está consultando mapas, calculando presupuestos y estructurando tus {dias} días en {destino}..."):
            try:
                # Prompt de Ingeniería de Viajes
                prompt_viajes = ChatPromptTemplate.from_messages([
                    ("system", (
                        "Sos un agente de viajes experto y concierge internacional de alta gama.\n"
                        "Tu tarea es armar un itinerario detallado, realista y lógicamente secuenciado día por día "
                        "basándote estrictamente en las variables provistas por el usuario.\n\n"
                        "Debes estructurar tu respuesta en formato Markdown usando las siguientes secciones estrictas:\n"
                        "1. **Resumen del Viaje**: Destino, días totales, estilo seleccionado y viabilidad del presupuesto real para ese destino.\n"
                        "2. **Desglose Estimado de Costos**: Tabla en Markdown que divida el presupuesto total de forma razonable: [Categoría (Alojamiento, Comida, Actividades, Transporte Local) | Porcentaje | Costo Estimado en USD].\n"
                        "3. **Itinerario Día por Día**: Para cada día (Día 1, Día 2, etc.), dividí obligatoriamente en [Mañana], [Tarde] y [Noche]. Detallá atracciones reales y optimizá las rutas para que los lugares queden cerca geográficamente.\n"
                        "4. **Recomendaciones Locales y Restricciones**: Consejos de transporte rápido, costumbres locales y respuestas específicas a las restricciones/preferencias indicadas por el usuario.\n\n"
                        "Mantené un tono profesional, entusiasta y muy preciso con los nombres de locaciones."
                    )),
                    ("human", (
                        "Por favor planificá mi viaje con estos datos:\n"
                        "- **Destino**: {destino}\n"
                        "- **Duración**: {dias} días\n"
                        "- **Presupuesto Total**: {presupuesto} USD\n"
                        "- **Estilo**: {estilo}\n"
                        "- **Restricciones/Notas**: {restricciones}"
                    ))
                ])

                # Ejecución directa de la cadena
                chain = prompt_viajes | llm
                respuesta_itinerario = chain.invoke({
                    "destino": destino,
                    "dias": dias,
                    "presupuesto": presupuesto,
                    "estilo": estilo_viaje,
                    "restricciones": restricciones if restricciones.strip() else "Ninguna especificada"
                })

                st.session_state.itinerario_resultado = respuesta_itinerario.content

            except Exception as e:
                st.error(f"Error generando el itinerario de viaje: {e}")

# 4. Renderizado del Reporte Final
if "itinerario_resultado" in st.session_state:
    st.subheader("📋 Tu Plan de Viaje Personalizado")
    st.markdown(st.session_state.itinerario_resultado)
else:
    st.info(
        "💡 Completá los datos de tu viaje en el panel superior y dale a 'Generar Itinerario Optimizado' para que la IA diseñe tu ruta.")