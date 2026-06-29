# 📓 Notas de Ingeniería & Aprendizajes: Proyecto 07

## 🎯 El Desafío Técnico
A diferencia de los proyectos RAG anteriores (donde se fragmentaba el texto en chunks pequeños para responder preguntas puntuales), el análisis de contratos requiere una **comprensión holística del documento**. Dividir un contrato en bloques puede hacer que el sistema pierda la relación entre una penalización (página 5) y una causa de rescisión (página 2). El desafío radicó en diseñar un pipeline de inyección completa aprovechando las ventanas de contexto extendidas de los modelos modernos.

## 🧱 Decisiones de Arquitectura & Por qué las tomé

### 1. Inyección de Contexto Completo en lugar de Vectorización (No-RAG Pipeline)
* **Decisión:** Para contratos de tamaño estándar (hasta 30-40 páginas), decidí no fragmentar el texto en una base de datos vectorial. En su lugar, el texto se extrae por completo y se pasa directo en el prompt al LLM.
* **Impacto:** Al usar `llama-3.3-70b-versatile` con su amplia ventana de contexto, el modelo analiza las cláusulas de forma interconectada, logrando detectar contradicciones o riesgos cruzados que un sistema de troceo vectorial (chunks) se hubiera salteado.

### 2. Temperatura Ultra Baja (`temperature=0.1`)
* **Decisión:** Seteé la temperatura de la API de Groq casi a cero.
* **Impacto:** En el ámbito legal no hay lugar para la creatividad. Necesitamos un comportamiento determinista. Si una cláusula de renovación automática no está en el PDF, el modelo debe decir firmemente que no está, eliminando la ventana de alucinación del LLM.

### 3. Salida Estructurada Basada en Plantilla Estricta
* **Decisión:** Obligué al sistema a través del prompt a responder usando componentes específicos de Markdown (especialmente tablas con esquemas fijos de criticidad).
* **Impacto:** Esto transforma un flujo de texto aburrido en un entregable de negocio real (un dashboard de riesgos visualizable en Streamlit), idóneo para procesos de due diligence corporativos.