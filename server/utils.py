import os
from pathlib import Path

import chromadb
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import BSHTMLLoader, TextLoader

from config import DATA_DIR

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=500,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

# Initialize the RAG database
def init_vectordb(embeddings_fn, path="./chroma/"):
    chroma_client = chromadb.PersistentClient(path=path)
    chroma_client.reset() 

    db = chroma_client.create_collection(
        name="it_support",
        embedding_function=embeddings_fn,
    )     
    
    doc_cnt = load_static_data(db)
    
    return db, doc_cnt


def load_static_data(db):
    data = []

    # Load html files from the data directory
    html_files = Path(DATA_DIR).glob('*.html')
    for html_file in html_files:    
        print(f"Loading {html_file}")
        loader = BSHTMLLoader(str(html_file))
        data.extend(loader.load())
    
    text_files = Path(DATA_DIR).glob('*.txt')
    for text_file in text_files:
        print(f"Loading {text_file}")
        loader = TextLoader(str(text_file))
        data.extend(loader.load())
        
    # Split documents and add to the database
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    data_chunks = text_splitter.split_documents(data)

    doc_ids = ["init_"+str(i) for i in range(len(data_chunks))]
    
    db.add(
        documents=[chunk.page_content for chunk in data_chunks], 
        # metadata=[dict(chunk).get("metadata", {}) for chunk in data_chunks],
        ids=doc_ids)
    
    return len(doc_ids)


def add_documents_to_vectordb(documents, db, metadata=None, doc_cnt=0):
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    # split_docs = text_splitter.split_documents(documents)
    # db.add_documents(
        # split_docs)
    
    db.add(
        documents=[documents],
        # metadata=metadata or {},
        ids=["msg_"+str(doc_cnt+1)]
    )
    
    return doc_cnt+1


def query_documents_from_vectordb(query, db, k=3):
    
    docs = db.query(
        query_texts=[query],
        n_results=k,
        # where={"metadata_field": "is_equal_to_this"},
        # where_document={"$contains":"search_string"}
    )

    return docs['documents']