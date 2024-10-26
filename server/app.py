import os
from flask import Flask, request, jsonify

from utils import init_vectordb, add_documents_to_vectordb
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

app = Flask(__name__)

# Initialize the RAG database when the server starts
rag_db = init_vectordb(embeddings)

@app.route('/')
def home():
    return "RAG-enabled Flask Server is running!"

if __name__ == '__main__':
    app.run(debug=True)
