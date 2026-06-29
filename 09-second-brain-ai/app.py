import streamlit as st
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Configuración de Entorno e Interfaz
load_dotenv()
st.set_page_config(page_title="Second Brain Knowledge Graph", page_icon="🧠", layout="wide")

st.title("🧠 Second Brain AI: Gráfico de Conocimiento")
st.write(
    "Escribí o pegá tus notas de estudio, reuniones o ideas sueltas. La IA extraerá los conceptos clave y cómo se interconectan.")

if not os.getenv("GROQ_API_KEY"):
    st.error("Falta la API Key de Groq. Configurala en tu archivo .env en la raíz del proyecto.")
    st.stop()


@st.cache_resource
def iniciar_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)


llm = iniciar_llm()

# 2. Área de Entrada de Notas
st.subheader("📝 Ingresá tu Nota o Pensamiento")
nota_usuario = st.text_area(
    "Pegá tus apuntes acá abajo:",
    height=200,
    placeholder=(
        "Ejemplo: LangChain es un framework de orquestación que permite conectar LLMs como Llama 3.3 con bases de datos vectoriales. "
        "ChromaDB es una base de datos vectorial que guarda embeddings locales. El Proyecto 06 usa ChromaDB para persistir el conocimiento."
    )
)

if st.button("🕸️ Construir Mapa de Conocimiento"):
    if not nota_usuario.strip():
        st.warning("Por favor, ingresá algún texto para poder mapear tu cerebro.")
    else:
        with st.spinner("La IA está leyendo tu mente, extrayendo conceptos y tejiendo la red de relaciones..."):
            try:
                # Prompt estricto de extracción de grafos en JSON limpio
                prompt_grafo = ChatPromptTemplate.from_messages([
                    ("system", (
                        "Sos un motor avanzado de extracción de Gráficos de Conocimiento (Knowledge Graphs).\n"
                        "Tu objetivo es leer la nota del usuario y extraer entidades (nodos) y las relaciones directas entre ellas (aristas/edges).\n\n"
                        "Debes responder ÚNICAMENTE con un objeto JSON válido que contenga una lista de relaciones, con la siguiente estructura exacta:\n"
                        "{{\n"
                        "  \"relaciones\": [\n"
                        "    {{\"origen\": \"Concepto A\", \"relacion\": \"usa / es_un / mapea\", \"destino\": \"Concepto B\"}}\n"
                        "  ]\n"
                        "}}\n"
                        "Reglas estrictas:\n"
                        "1. No agregues ninguna introducción, explicación ni formateo Markdown (no uses ```json).\n"
                        "2. Mantené los nombres de las entidades cortos y concisos (1 a 3 palabras máximo).\n"
                        "3. Extraé la mayor cantidad de conexiones lógicas válidas que encuentres en el texto."
                    )),
                    ("human", "Acá está la nota para procesar:\n\n{texto_nota}")
                ])

                chain = prompt_grafo | llm
                respuesta = chain.invoke({"texto_nota": nota_usuario})

                # Limpieza de seguridad por si el modelo devuelve código markdown envuelto
                raw_content = respuesta.content.strip()
                if raw_content.startswith("```json"):
                    raw_content = raw_content.replace("```json", "").replace("```", "").strip()

                datos_grafo = json.loads(raw_content)
                st.session_state.datos_grafo = datos_grafo["relaciones"]

            except Exception as e:
                st.error(f"Error procesando el gráfico semántico: {e}\nRespuesta cruda de la IA: {respuesta.content}")

# 3. Renderizado y Visualización del Gráfico de Red
if "datos_grafo" in st.session_state and st.session_state.datos_grafo:
    relaciones = st.session_state.datos_grafo

    st.success("¡Estructura semántica extraída con éxito!")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 📊 Relaciones Detectadas")
        for rel in relaciones:
            st.markdown(f"* **{rel['origen']}** —_({rel['relacion']})_→ **{rel['destino']}**")

    with col2:
        st.markdown("### 🕸️ Mapa de Nodos Interconectados")

        # Inicializamos el objeto grafo de NetworkX
        G = nx.DiGraph()

        for rel in relaciones:
            G.add_edge(rel["origen"], rel["destino"], label=rel["relacion"])

        # Layout de distribución elástica para evitar que los nodos se pisen
        pos = nx.spring_layout(G, k=0.8, seed=42)

        fig, ax = plt.subplots(figsize=(10, 7), facecolor="#0e1117")
        ax.set_facecolor("#0e1117")

        # Dibujamos los nodos con estética moderna
        nx.draw_networkx_nodes(G, pos, node_size=2500, node_color="#4361ee", ax=ax)
        nx.draw_networkx_edges(G, pos, width=2, edge_color="#888888", arrowsize=20, ax=ax)

        # Etiquetas de los conceptos (Nodos)
        nx.draw_networkx_labels(G, pos, font_size=10, font_color="#ffffff", font_weight="bold", ax=ax)

        # Etiquetas de las flechas (Relaciones)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="#cccccc",
                                     bbox=dict(facecolor="#1e222b", alpha=0.8, edgecolor="none"))

        plt.axis('off')
        st.pyplot(fig)
else:
    st.info("💡 Introducí una nota arriba y activá el constructor para empezar a graficar tu conocimiento.")