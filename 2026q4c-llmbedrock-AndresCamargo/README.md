# Asistente Conversacional Especializado en RAG con Amazon Bedrock

Este proyecto implementa una aplicación web con interfaz de chat (Streamlit) que actúa como un asistente experto en **RAG (Retrieval-Augmented Generation)**. Utiliza el modelo **Amazon Nova Lite** para la generación de respuestas y **Amazon Titan Text Embeddings V2** para la búsqueda semántica en documentos, todo desplegado sobre **Amazon Bedrock**.

## Arquitectura y Funcionamiento (RAG)

El sistema implementa el patrón RAG en tres fases principales:

1. **Ingesta y Vectorización (Ingest):** Se cargan documentos PDF locales, se dividen en fragmentos (chunks) y se convierten en vectores (embeddings) usando Amazon Titan. Estos vectores se almacenan en un índice local usando **FAISS** (Facebook AI Similarity Search).
2. **Recuperación (Retrieval):** Cuando el usuario hace una pregunta, el sistema busca en el índice FAISS los fragmentos de texto más relevantes semánticamente.
3. **Aumentación y Generación (Augmented Generation):** Los fragmentos recuperados se inyectan como "contexto" en el prompt que se envía a Amazon Nova Lite. El modelo genera una respuesta basada **estrictamente** en la información de los documentos, reduciendo las alucinaciones.

## Tecnologías Utilizadas

* **Python 3.11+**
* **Streamlit:** Interfaz gráfica y gestión del historial de chat.
* **Amazon Bedrock:** Servicio de AWS para invocar los Modelos Fundacionales.
* **LangChain & FAISS:** Para la orquestación del flujo RAG y la base de datos vectorial.
* **Docker:** Para la contenerización y despliegue local.

## Requisitos Previos

* Cuenta de AWS con acceso a Amazon Bedrock (modelos Nova Lite y Titan Embeddings habilitados en la región `us-east-1`).
* Credenciales de AWS (API Key de corta/durabilidad o credenciales IAM).
* Docker instalado (opcional, para despliegue en contenedor).

## Configuración del Entorno

1. Clonar este repositorio e ingresa a la carpeta del proyecto.
2. Crear un entorno virtual de Python e instala las dependencias:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
 3. **Iniciar la aplicación:**
   ```bash
   streamlit run app.py
   ```
   La aplicación estará disponible en `http://localhost:8501`.

## 🐳 Despliegue con Docker

Si considera que es mejor ejecutar la aplicación en un contenedor aislado:

1. **Construir la imagen:**
   ```bash
   docker build -t rag-bedrock .
   ```
2. **Ejecutar el contenedor:**
   ```bash
   docker run --env-file .env -p 8501:8501 rag-bedrock
   ```

## Estructura del Proyecto

```text
├── data/                  # Carpeta con los PDFs fuente de conocimiento
├── faiss_index/           # Base de datos vectorial generada (ignorada en Git)
├── .env                   # Credenciales de AWS (ignorado en Git)
├── .env.example           # Plantilla de variables de entorno
├── .gitignore             # Archivos excluidos del control de versiones
├── app.py                 # Código principal de la interfaz Streamlit
├── ingest.py              # Script para procesar PDFs y generar embeddings
├── Dockerfile             # Configuración para construir la imagen Docker
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación del proyecto
```

## Notas de Seguridad

* Las credenciales de AWS se manejan exclusivamente mediante variables de entorno.
* El archivo `.env` y la carpeta `venv/` están excluidos del repositorio mediante `.gitignore`.
* Al finalizar el uso de la aplicación, se recomienda revocar la API Key de Bedrock en la consola de AWS para evitar consumos no deseados.