# Proyecto 4: Extractor Inteligente de Gastos (AI Vision)

Aplicación que utiliza **Modelos de Visión Multimodal** para procesar imágenes de tickets o facturas, extraer su información de forma estructurada (JSON) mediante **Pydantic** y presentar los datos limpios al usuario.

## 🛠️ Tecnologías utilizadas
- **LLM de Visión:** Groq (`llama-3.2-11b-vision-preview`)
- **Estructuración de Datos:** Pydantic & LangChain Structured Outputs
- **Procesamiento de Imágenes:** Pillow (PIL)
- **Interfaz:** Streamlit

## 🚀 Cómo ejecutar
1. Activa el entorno: `source venv/bin/activate`
2. Instala las dependencias: `pip install -r requirements.txt`
3. Configura tu `GROQ_API_KEY` en el `.env`
4. Corre la app: `streamlit run app.py`



<img width="1440" height="900" alt="Image" src="https://github.com/user-attachments/assets/050bc3fb-68c8-41c7-ba55-067462337fd9" />
