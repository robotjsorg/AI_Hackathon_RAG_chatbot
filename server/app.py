import os
from flask import Flask, request, jsonify

from utils import init_vectordb, add_documents_to_vectordb
import chromadb.utils.embedding_functions as embedding_functions

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
embed_fn = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-3-small"
            )


app = Flask(__name__)

global doc_cnt
# Initialize the RAG database when the server starts
rag_db, doc_cnt = init_vectordb(embed_fn)

@app.route('/')
def home():
    return "RAG-enabled Flask Server is running!"

@app.route('/add_documents', methods=['POST'])
def add_documents():
    global doc_cnt
    data = request.json
    
    add_documents_to_vectordb(data, rag_db, doc_cnt=doc_cnt)
    
    return "Documents added to vector database"

@app.route('/retrieve', methods=['POST'])
def retrieve_documents():
    data = request.json
    context = retrieve_documents_from_vectordb(data, rag_db)
    return context

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
