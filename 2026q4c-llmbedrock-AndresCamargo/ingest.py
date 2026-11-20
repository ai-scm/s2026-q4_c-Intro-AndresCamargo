# ingest.py
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
import boto3

# Cargar variables de entorno
load_dotenv()

def construir_indice():
    print("📄 1. Cargando documentos de la carpeta 'data/'...")
    loader = PyPDFDirectoryLoader("./data")
    docs = loader.load()
    print(f"   -> Se cargaron {len(docs)} páginas en total.")

    print("✂️ 2. Partiendo el texto en chunks (trozos)...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(f"   -> Se dividió en {len(splits)} trozos de texto.")

    print("🔢 3. Generando embeddings con Amazon Titan y guardando en FAISS...")
    # Crear el cliente de Bedrock
    bedrock_client = boto3.client(
        "bedrock-runtime", 
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    
    # Usar el modelo de embeddings de Amazon
    bedrock_embeddings = BedrockEmbeddings(
        client=bedrock_client,
        model_id=os.getenv("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")
    )
    
    # Crear la base de datos vectorial
    vectorstore = FAISS.from_documents(splits, bedrock_embeddings)
    
    # Guardar el índice en el disco duro para no tener que procesar los PDFs de nuevo
    vectorstore.save_local("faiss_index")
    print("✅ ¡Índice creado exitosamente! Ya puedes correr 'streamlit run app.py'")

if __name__ == "__main__":
    construir_indice()