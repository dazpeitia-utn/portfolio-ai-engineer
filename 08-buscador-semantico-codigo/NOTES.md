# 📓 Notas de Ingeniería & Aprendizajes: Proyecto 08

## 🎯 El Desafío Técnico
Los textos planos se separan por puntos o saltos de línea. Sin embargo, hacer eso en código fuente rompe por completo la lógica (por ejemplo, separando una declaración `if` de su bloque de ejecución o dejando un `try` sin su `except`). El desafío de este proyecto fue implementar un indexador que entienda la semántica y la estructura de un archivo de programación.

## 🧱 Decisiones de Arquitectura & Por qué las tomé

### 1. Separadores Especializados (`Language.PYTHON`)
* **Decisión:** Utilicé el método de factoría estática `from_language` provisto por LangChain.
* **Impacto:** Al indicarle al splitter el lenguaje de destino, este prioriza los tokens de división lógicos (`def`, `class`, llaves, tabulaciones). Así, el bloque de código resultante viaja al espacio vectorial manteniendo cohesión lógica interna.

### 2. Motor Vectorial In-Memory con FAISS
* **Decisión:** Reemplacé ChromaDB por **FAISS** en memoria para este pipeline.
* **Impacto:** Para búsquedas rápidas en archivos locales cargados en la sesión actual, no requerimos persistir bases de datos pesadas en disco. FAISS ofrece una velocidad de comparación de similitud imbatible corriendo directamente sobre estructuras de arrays nativos.

### 3. Recuperación Semántica vs. "Ctrl + F" (Grep)
* **Decisión:** El buscador no usa expresiones regulares ni coincidencia exacta de strings.
* **Impacto:** Si buscás *"guardar datos en storage"*, el sistema es capaz de traerte un bloque de código que use comandos como `shutil.rmtree` o `with open("file", "wb")` aunque la palabra "storage" jamás figure en el código escrito. El mapa de embeddings comprende la intención del algoritmo.