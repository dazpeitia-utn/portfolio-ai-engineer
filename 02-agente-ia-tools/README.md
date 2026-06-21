# 🤖 Proyecto 02: Agente de IA con Herramientas (Tool Calling & ReAct)

Este proyecto consiste en un **Agente de Inteligencia Artificial Autónomo** desarrollado con **LangChain** y **Streamlit**. A diferencia de las arquitecturas rígidas, este agente implementa un bucle de razonamiento activo que le permite evaluar el requerimiento del usuario y decidir por sí mismo qué herramientas externas necesita invocar para resolver problemas complejos.

## 🧠 Conceptos de IA Aplicados
* **Framework ReAct (Reasoning and Acting):** Paradigma que combina la generación de trazas de razonamiento lógico ("Pensar") con la ejecución de acciones específicas de herramientas ("Actuar").
* **Tool Calling / Function Calling:** Capacidad del LLM para estructurar argumentos y delegar tareas técnicas a funciones de código externas en lugar de alucinar respuestas.
* **Agent Executor:** Orquestador en tiempo real que maneja el estado del agente, pasa las observaciones de las herramientas de regreso al modelo y gestiona los errores de parseo.

## 🛠️ Tecnologías y Librerías Utilizadas
* **LangChain Agents:** Módulo especializado para la creación de cadenas reactivas y agentes inteligentes.
* **ChatGroq (LLM):** Inferencia de ultra baja latencia con el modelo de código abierto `llama-3.1-8b-instant`.
* **DuckDuckGo Search API:** Herramienta de navegación web integrada para la recuperación de información pública en tiempo real sin costo de suscripción.
* **Streamlit:** Interfaz de usuario interactiva y dinámica.

## 🚀 Instrucciones de Ejecución

1. Configura tu variable de entorno en el archivo `.env` de esta carpeta:
   ```env
   GROQ_API_KEY=tu_gsk_api_key_aqui