# 📓 Notas de Ingeniería & Aprendizajes: Proyecto 09

## 🎯 El Desafío Técnico
Los sistemas RAG tradicionales asumen que la información relevante se encuentra confinada dentro de un vector aislado en el espacio hiperdimensional. Sin embargo, el conocimiento humano es interconectado por naturaleza. El desafío de este proyecto fue romper el paradigma lineal del chunking vectorial para entrar en el terreno de la **Teoría de Grafos (Knowledge Graphs)**, mapeando cómo las ideas se relacionan explícitamente entre sí mediante estructuras de tripletas (Sujeto, Predicado, Objeto).

## 🧱 Decisiones de Arquitectura & Por qué las tomé

### 1. Extracción Estricta de Payloads JSON
* **Decisión:** Diseñé un prompt del sistema blindado que prohíbe taxativamente explicaciones conversacionales del LLM, obligándolo a emitir un string JSON puro estructurado en diccionarios de origen, relación y destino.
* **Impacto:** Permite automatizar tuberías de datos de manera determinista. La salida cruda de la API de Groq puede pasar directo a un método `json.loads()` sin romper el intérprete de Python, facilitando la conversión de lenguaje natural a tipos de datos complejos nativos del backend.

### 2. Uso de NetworkX y Distribuciones de Fuerzas (Spring Layout)
* **Decisión:** Integré `networkx` para modelar un grafo dirigido (`DiGraph()`) y apliqué un algoritmo de distribución elástica basado en fuerzas de repulsión eléctrica.
* **Impacto:** Los grafos tienden a colapsar visualmente si los nodos se superponen. La física del `spring_layout` empuja los conceptos relacionados cerca y repele los ajenos, maximizando la legibilidad de la red semántica dentro de la interfaz del portafolio.

### 3. Del Vector al Grafo (Hacia GraphRAG)
* **Decisión:** Almacenar entidades explícitas en lugar de proximidad geométrica de texto.
* **Impacto:** Este proyecto sienta las bases fundamentales de arquitecturas avanzadas como **GraphRAG**. El modelo ya no solo "busca similitudes de palabras sueltas", sino que entiende la semántica de las dependencias estructurales de una idea de negocio o de ingeniería.

---

## 🛠️ Lecciones de Infraestructura y VirtualEnvs en macOS
* **Aprendizaje (El choque de Pythons locales):** Al instalar librerías nativas complejas (`matplotlib`, `networkx`) en monorepositorios, el comando global `pip` de la terminal puede corromperse o apuntar al intérprete del sistema operativo en lugar de al entorno virtual de la raíz.
* **Solución de Ingeniería:** Aprendí a mitigar este desvío ejecutando la instalación directamente mediante el binario absoluto del entorno (`./venv/bin/python -m pip install...`). Esto garantiza un aislamiento hermético de las dependencias de IA y evita fugas de contexto o falsos errores de `ModuleNotFoundError` al levantar la interfaz con Streamlit.