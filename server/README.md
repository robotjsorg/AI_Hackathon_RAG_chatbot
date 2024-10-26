This is a Flask-based server that implements a Retrieval-Augmented Generation (RAG) system for document storage and retrieval.

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

3. Run the server:

```bash
python app.py
```

## API Endpoints

### 1. Home

- **URL:** `/`
- **Method:** GET
- **Description:** Check if the server is running.
- **Response:** "RAG-enabled Flask Server is running!"

### 2. Add Documents

- **URL:** `/add_documents`
- **Method:** POST
- **Description:** Add new documents to the vector database.
- **Request Body:** JSON object containing documents to be added.
- **Response:** "Documents added to vector database"

### 3. Retrieve Documents

- **URL:** `/retrieve`
- **Method:** POST
- **Description:** Query the vector database to retrieve relevant documents.
- **Request Body:** JSON object containing the query.
- **Response:** JSON object with retrieved context.

## Implementation Details

The server uses the following components:

1. **Vector Database:** Initialized using the `init_vectordb` function from the `utils` module.
2. **Embedding Function:** Uses OpenAI's embedding model "text-embedding-3-small".
3. **Document Counter:** Keeps track of the number of documents added to the database.

