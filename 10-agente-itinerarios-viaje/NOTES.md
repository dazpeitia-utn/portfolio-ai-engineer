# 📓 Notas de Ingeniería & Aprendizajes: Proyecto 10

## 🎯 El Desafío Técnico
Los problemas tradicionales de NLP suelen procesar un solo flujo de entrada (por ejemplo, resumir un texto largo). Sin embargo, las aplicaciones del mundo real requieren que los modelos actúen como **motores de optimización multi-variable**, resolviendo ecuaciones de lógica difusa donde el presupuesto interfiere con las actividades de un destino y las restricciones de salud o tiempo limitan los alcances geográficos del día a día.

## 🧱 Decisiones de Arquitectura & Por qué las tomé

### 1. Ajuste Dinámico de Temperatura (`temperature=0.3`)
* **Decisión:** Elevé levemente la temperatura de `0.1` (usada en proyectos legales/de código) a `0.3`.
* **Impacto:** Un itinerario de viaje necesita un balance sutil. No queremos alucinaciones de lugares ficticios (precisión), pero sí requerimos que el modelo proponga combinaciones fluidas de restaurantes y paseos alternativos atractivos (creatividad controlada).

### 2. Estructura de Formulario Bidimensional en Streamlit
* **Decisión:** Segmenté los inputs usando controles de UI especializados (`st.slider`, `st.number_input`, `st.selectbox`) distribuidos en dos columnas balanceadas.
* **Impacto:** Al recolectar datos pre-validados del lado del cliente, se minimiza la cantidad de ruido sintáctico que llega a las variables de inyección del prompt, garantizando que el LLM reciba un payload estructurado y limpio.

### 3. Matriz de Distribución Presupuestaria Financiera
* **Decisión:** Obligué al modelo a través del prompt del sistema a desglosar porcentajes de gastos comerciales en una tabla Markdown coherente.
* **Impacto:** Esto fuerza al LLM a ejecutar una subtarea analítica previa de estimación matemática financiera antes de redactar las actividades del día a día, lo que estabiliza su coherencia lógica y disminuye la posibilidad de proponer actividades de lujo imposibles de costear con presupuestos bajos.