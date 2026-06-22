import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import base64
import io

# Componentes de LangChain y Pydantic
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import Optional, List

# 1. Cargar variables de entorno
load_dotenv()

st.set_page_config(page_title="AI Expense Tracker", page_icon="🧾", layout="wide")
st.title("🧾 Extractor Inteligente de Gastos con IA de Visión")
st.write("Sube la foto de cualquier ticket o factura y la IA extraerá los datos de forma estructurada.")

if not os.getenv("GROQ_API_KEY"):
    st.error("Por favor, configura tu GROQ_API_KEY en el archivo .env")
    st.stop()


# Esquema para el filtrado personalizado de palabras clave
class FiltroPalabra(BaseModel):
    palabra_clave: str = Field(description="La palabra clave solicitada por el usuario")
    valor_asociado: str = Field(
        description="El valor, número, precio o texto que aparece inmediatamente al lado o asociado a esa palabra clave en el ticket")


# 2. Definir el esquema de datos principal (Pydantic mejorado)
class TicketData(BaseModel):
    comercio: str = Field(description="Nombre del comercio o empresa que emite el ticket")
    fecha: Optional[str] = Field(description="Fecha de la compra en formato DD/MM/AAAA si está disponible")
    categoria: str = Field(
        description="Categoría del gasto (ej. Supermercado, Combustible, Restaurante, Servicios, etc.)")
    items: List[str] = Field(description="Lista de los principales productos o servicios comprados")
    total: float = Field(description="El monto total cobrado, expresado como número flotante (sin signos de moneda)")
    filtros_personalizados: List[FiltroPalabra] = Field(
        description="Lista de los filtros por palabra clave solicitados por el usuario con sus valores asociados")
    resumen_analisis: str = Field(description="Un breve comentario o consejo sobre el gasto realizado")


# Inicializar el modelo activo de producción según la documentación de Groq 2026
llm = ChatGroq(model="qwen/qwen3.6-27b", temperature=0.1)

# Vincular el modelo con nuestro esquema de Pydantic para forzar la salida estructurada
structured_llm = llm.with_structured_output(TicketData)


# Función auxiliar para convertir la imagen de Streamlit a Base64
def encode_image_to_base64(uploaded_file):
    image = Image.open(uploaded_file)
    buffered = io.BytesIO()
    image.convert("RGB").save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


# 3. Interfaz de usuario (Streamlit)
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 Subir Ticket")
    uploaded_file = st.file_uploader("Elige una imagen (JPG, PNG)", type=["jpg", "jpeg", "png"])

    # NUEVO: Input para las palabras clave personalizadas
    st.subheader("🔍 Filtrado por Palabras Clave")
    keywords_input = st.text_input(
        "Introduce palabras clave separadas por comas (ej: V-POWER, IVA, C.U.I.T, Hora)",
        placeholder="V-POWER, IVA, C.U.I.T"
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Ticket cargado", width="stretch")

with col2:
    st.header("📊 Datos Extraídos")

    if uploaded_file is not None:
        if st.button("🚀 Analizar Ticket con IA"):
            with st.spinner("La IA está leyendo y analizando el ticket con tus filtros..."):
                try:
                    # Convertir imagen a base64
                    base64_image = encode_image_to_base64(uploaded_file)

                    # Armar la instrucción de los filtros si el usuario escribió algo
                    instruccion_filtros = ""
                    if keywords_input:
                        instruccion_filtros = f"\nCRÍTICO: Además de los datos generales, busca específicamente las siguientes palabras clave e identifica qué valor o monto tienen asociado en el ticket: {keywords_input}."

                    # Construir el mensaje multimodal (Texto + Imagen)
                    message = {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Analiza minuciosamente esta imagen de un ticket y extrae la información requerida en el esquema estructurado.{instruccion_filtros}"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }

                    # Invocar al modelo estructurado
                    resultado: TicketData = structured_llm.invoke([message])

                    # Mostrar los resultados generales
                    st.success("¡Datos extraídos con éxito!")
                    st.metric(label="Total Gastado", value=f"$ {resultado.total:,.2f}")
                    st.subheader(f"🏪 {resultado.comercio}")
                    st.caption(f"📅 Fecha: {resultado.fecha or 'No detectada'} | 🏷️ Categoría: {resultado.categoria}")

                    st.write("**🛒 Ítems detectados:**")
                    for item in resultado.items:
                        st.write(f"- {item}")

                    # NUEVO: Mostrar los filtros personalizados encontrados
                    if resultado.filtros_personalizados:
                        st.write("---")
                        st.write("🔍 **Valores para tus Palabras Clave:**")
                        for filtro in resultado.filtros_personalizados:
                            st.markdown(f"* **{filtro.palabra_clave}:** `{filtro.valor_asociado}`")

                    st.write("---")
                    st.info(f"💡 **Análisis de la IA:** {resultado.resumen_analisis}")

                except Exception as e:
                    st.error(f"Hubo un error al procesar la imagen: {e}")
    else:
        st.info("👋 Sube una imagen en la columna de la izquierda y haz clic en 'Analizar Ticket' para ver la magia.")