import streamlit as st
import boto3
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings

load_dotenv()

st.title("📚 Asistente Experto en RAG")
st.caption("Potenciado por Amazon Bedrock (Nova Lite + Titan Embeddings)")

@st.cache_resource
def get_retriever():
    bedrock_client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))
    bedrock_embeddings = BedrockEmbeddings(
        client=bedrock_client,
        model_id=os.getenv("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")
    )
    vectorstore = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

retriever = get_retriever()
bedrock_client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))
MODEL_ID = os.getenv("MODEL_ID", "amazon.nova-lite-v1:0")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pregúntame sobre RAG..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Buscando en los documentos y pensando..."):
            try:
                docs = retriever.invoke(prompt)
                contexto = "\n\n".join([doc.page_content for doc in docs])

                system_prompt = f"""Eres un experto en Inteligencia Artificial y RAG. 
                Responde la pregunta del usuario utilizando ÚNICAMENTE el siguiente contexto extraído de los documentos:
                
                CONTEXTO:
                {contexto}
                
                Si la respuesta no está en el contexto, di: "Lo siento, no encontré esa información en los documentos proporcionados"."""

                # Formatear los mensajes para Bedrock
                formatted_messages = []
                for msg in st.session_state.messages:
                    formatted_messages.append({
                        "role": msg["role"],
                        "content": [{"text": msg["content"]}]
                    })

                response = bedrock_client.converse(
                    modelId=MODEL_ID,
                    messages=formatted_messages,
                    system=[{"text": system_prompt}]
                )
                
                respuesta = response['output']['message']['content'][0]['text']
                st.markdown(respuesta)
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
            except Exception as e:
                st.error(f"Error: {e}")