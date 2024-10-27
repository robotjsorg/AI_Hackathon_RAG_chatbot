import os
from flask import Flask, request, jsonify
import ollama
from utils import init_vectordb, add_documents_to_vectordb, query_documents_from_vectordb
import chromadb.utils.embedding_functions as embedding_functions

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Define the custom embedding function
class OllamaEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, model_name: str = 'llama3.2'):
        self.model_name = model_name

    def __call__(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        embeddings = []
        for text in texts:
            response = ollama.embed(model=self.model_name, input=text)
            # Check if the response contains an embedding
            if 'embedding' in response:
                embedding = response['embedding']
                embeddings.append(embedding)
            else:
                # Handle the case where embedding is not returned
                embeddings.append([])  # Or handle appropriately
        return embeddings

embed_fn = OllamaEmbeddingFunction(model_name='llama3.2')

# embed_fn = embedding_functions.OpenAIEmbeddingFunction(
#                 api_key=os.getenv("OPENAI_API_KEY"),
#                 model_name="text-embedding-3-small"
#             )


app = Flask(__name__)

global doc_cnt
# Initialize the RAG database when the server starts
rag_db, doc_cnt = init_vectordb(embed_fn)

@app.route('/')
def home():
    return "RAG-enabled Flask Server is running!"

@app.route('/add_documents', methods=['POST'])
def add_documents():
    try:
        global doc_cnt
        data = request.json
        message = data.get("message")
        add_documents_to_vectordb(message, rag_db, doc_cnt=doc_cnt)
        doc_cnt += 1
        
        return "Documents added to vector database"
    
    except Exception as e:
        
        return jsonify({"error": str(e)}), 500
    

@app.route('/retrieve', methods=['POST'])
def retrieve_documents():
    data = request.json
    query = data.get("query")
    context = query_documents_from_vectordb(query, rag_db)
    
    return context


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)