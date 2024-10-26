import chromadb
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Initialize the RAG database
def init_vectordb(embeddings_function):
    persistent_client = chromadb.PersistentClient()

    db = Chroma(
        client=persistent_client,
        collection_name="it_support",
        embedding_function=embeddings_function,
    )
     
    return db


def add_documents_to_vectordb(documents, db):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(documents)
    db.add_documents(split_docs)
    db.persist()

