# 📚 Document RAG System

A Retrieval-Augmented Generation (RAG) system that enables users to ask questions about PDF documents. The system processes documents, splits them into meaningful sentence-based chunks, generates embeddings, stores them in Elasticsearch, retrieves the most relevant chunks using vector similarity, and generates answers using an LLM.

## 🚀 Overview

This project demonstrates the end-to-end implementation of a **RAG pipeline**:

```text
PDF Documents
      │
      ▼
┌──────────────┐
│   Parsing    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Chunking   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Embeddings  │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Elasticsearch    │
│ Vector Index     │
└────────┬─────────┘
         │
         │ User Query
         ▼
┌──────────────┐
│ Query        │
│ Embedding    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Vector       │
│ Retrieval    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Context      │
│ Selection    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ LLM Response │
└──────────────┘
```

The project focuses on understanding the core components behind production-oriented RAG systems: **document processing, chunking, embeddings, vector search, context management, and grounded response generation**.

---

## ✨ Key Features

* 📄 PDF document text extraction
* ✂️ Sentence-based document chunking
* 🔢 Token counting using `tiktoken`
* 🧠 Text embedding generation
* 🔎 Elasticsearch vector similarity search
* 📦 Document and chunk metadata storage
* 🎯 Top-K relevant chunk retrieval
* 🧮 Context token-limit management
* 🤖 LLM-based response generation
* 🔁 Retry mechanism for embedding API failures
* 📝 YAML-based prompt configuration
* 📊 Logging throughout the pipeline
* 🔐 Environment-variable based configuration

---

## 🏗️ Project Architecture

```text
rag/
│
├── src/
│   │
│   ├── chunking/
│   │   └── chunking.py
│   │
│   ├── embedding/
│   │   └── embedder.py
│   │
│   ├── generation/
│   │   └── response_generation.py
│   │
│   ├── ingestion/
│   │   ├── indexing.py
│   │   └── ingestion.py
│   │
│   ├── parsing/
│   │   └── parsing.py
│   │
│   └── retrieval/
│       └── retrieval.py
│
├── configs/
│   └── prompts.yml
│
├── utils/
│   ├── __init__.py
│   └── utils.py
│
└── main.py
```

---

## 🔄 RAG Pipeline

### 1. Document Parsing

PDF documents are processed using PyMuPDF (`fitz`).

The parser:

* Opens the PDF
* Extracts text page-by-page
* Cleans the extracted text
* Calculates token counts
* Stores page-level information

```python
{
    "page_num": 0,
    "text": "...",
    "token_count": 250
}
```

---

### 2. Chunking

The extracted document is divided into sentence-based chunks.

The current implementation groups **5 sentences per chunk by default**.

```text
Document
   │
   ├── Page 1
   │     ├── Sentence 1
   │     ├── Sentence 2
   │     ├── Sentence 3
   │     ├── Sentence 4
   │     └── Sentence 5
   │
   └── Page 2
```

Each resulting chunk retains its page information, making it possible to associate retrieved content with its source page.

---

### 3. Embedding Generation

Each text chunk is converted into a numerical vector representation.

The embedding component:

* Counts tokens using `tiktoken`
* Truncates text exceeding the configured token limit
* Generates embeddings through the OpenAI embedding API
* Uses exponential backoff retries for failures

These vectors allow semantic similarity search over the document collection.

---

### 4. Elasticsearch Vector Indexing

The generated embeddings and metadata are stored in Elasticsearch.

The index stores:

```text
chunk_text
page_num
document_name
embedding
chunk_token_count
```

The embedding field is configured as an Elasticsearch `dense_vector`.

---

### 5. Query Retrieval

When a user submits a question:

```text
User Question
      │
      ▼
Query Embedding
      │
      ▼
Elasticsearch
      │
      ▼
Cosine Similarity
      │
      ▼
Top Relevant Chunks
```

The system retrieves the top relevant chunks using cosine similarity between the query embedding and stored document embeddings.

---

### 6. Context Selection

The retrieved chunks are accumulated until the configured context limit is reached.

This prevents the system from sending an unnecessarily large amount of retrieved text to the generation model.

```text
Retrieved Chunks
      │
      ├── Chunk 1
      ├── Chunk 2
      ├── Chunk 3
      ├── ...
      │
      ▼
Context Token Limit
      │
      ▼
Final Context
```

---

### 7. Response Generation

The selected document chunks are inserted into a YAML-configured prompt together with the user's question.

The LLM then generates the final response using the retrieved document context.

The prompt explicitly instructs the model to rely on the provided context and respond when the required information is unavailable.

---

## 🛠️ Tech Stack

| Technology            | Purpose                              |
| --------------------- | ------------------------------------ |
| **Python**            | Core implementation                  |
| **PyMuPDF**           | PDF text extraction                  |
| **spaCy**             | Sentence segmentation                |
| **OpenAI Embeddings** | Text vectorization                   |
| **Elasticsearch**     | Vector storage and similarity search |
| **tiktoken**          | Token counting                       |
| **PyYAML**            | Prompt configuration                 |
| **Tenacity**          | API retry mechanism                  |
| **python-dotenv**     | Environment configuration            |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd rag
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If a `requirements.txt` is not included, install the dependencies used by the project:

```bash
pip install openai elasticsearch pymupdf spacy tiktoken \
python-dotenv pyyaml tenacity
```

Download the spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key

ES_CLOUD_ID=your_elasticsearch_cloud_id
ES_API_KEY=your_elasticsearch_api_key
ES_INDEX_NAME=your_index_name

PDF_DIR=path/to/pdf/documents
```

**Never commit your `.env` file or API keys to GitHub.**

Add it to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Running the Project

Run:

```bash
python main.py
```

The main application:

1. Loads environment variables
2. Creates the Elasticsearch client
3. Ensures the Elasticsearch index exists
4. Runs the document ingestion pipeline when enabled
5. Converts the query into an embedding
6. Retrieves relevant document chunks
7. Builds the context
8. Generates the final LLM response

---

## 📥 Document Ingestion

To ingest PDFs into Elasticsearch, enable the ingestion flag in `main.py`:

```python
ingest_flag = True
```

The ingestion pipeline then performs:

```text
PDF
 │
 ▼
Parse
 │
 ▼
Clean Text
 │
 ▼
Split into Sentences
 │
 ▼
Create Chunks
 │
 ▼
Calculate Token Count
 │
 ▼
Generate Embedding
 │
 ▼
Store in Elasticsearch
```

After the documents have been indexed, ingestion can be disabled:

```python
ingest_flag = False
```

and the system can be used for querying.

---

## 🔎 Example Query

The application can query the indexed documents using a natural-language question such as:

```text
Sabka Saath, Sabka Vikas
```

The system retrieves semantically relevant chunks from Elasticsearch and provides them as context to the LLM.

---

## 📁 Module Responsibilities

### `src/parsing/parsing.py`

Responsible for extracting and formatting text from PDF documents.

### `src/chunking/chunking.py`

Responsible for sentence segmentation and creation of independent text chunks.

### `src/embedding/embedder.py`

Responsible for token-aware embedding generation and retry handling.

### `src/ingestion/ingestion.py`

Orchestrates the document ingestion workflow.

### `src/ingestion/indexing.py`

Creates the Elasticsearch index and stores document chunks and embeddings.

### `src/retrieval/retrieval.py`

Retrieves relevant chunks from Elasticsearch using vector similarity.

### `src/generation/response_generation.py`

Combines retrieved context with the user query and generates the final LLM response.

### `utils/utils.py`

Contains reusable utilities such as:

* Token counting
* Text formatting
* YAML prompt loading

### `configs/prompts.yml`

Contains the prompt template used during response generation.

### `main.py`

Acts as the application entry point and connects the major components of the RAG pipeline.

---

## 🧠 Concepts Demonstrated

This project demonstrates practical understanding of:

* Retrieval-Augmented Generation
* Semantic Search
* Vector Embeddings
* Vector Databases / Vector Search
* Elasticsearch Dense Vectors
* Cosine Similarity
* Document Parsing
* Chunking Strategies
* Token Management
* Prompt Engineering
* LLM Context Construction
* API Retry Strategies
* Environment Configuration
* Modular Python Architecture
* Logging and Error Handling

---

## 🎯 Why This Project?

Traditional LLM applications can struggle when answering questions about private or domain-specific documents.

RAG addresses this by separating the process into two stages:

```text
Retrieval
    ↓
Find relevant knowledge

Generation
    ↓
Generate an answer using that knowledge
```

Instead of relying only on information learned during model training, this application retrieves relevant information from the provided documents and uses it as context for response generation.

---

## 🔮 Future Improvements

Potential improvements for taking this project further include:

* Hybrid search combining keyword and vector retrieval
* Re-ranking retrieved chunks
* Metadata filtering
* Improved chunking strategies
* Query rewriting
* Conversation memory
* Streaming responses
* FastAPI backend
* Authentication and authorization
* Evaluation datasets and RAG evaluation metrics
* Observability and tracing
* Docker-based deployment
* Automated testing
* CI/CD pipeline
* Background document ingestion
* Support for additional document formats

---

## 💼 Resume Description

**Document RAG System — Python, Elasticsearch, OpenAI, spaCy**

> Built an end-to-end Retrieval-Augmented Generation (RAG) pipeline for querying PDF documents using sentence-based chunking, OpenAI embeddings, and Elasticsearch vector similarity search. Implemented token-aware context construction, metadata-based document tracking, configurable prompt templates, API retry handling, and modular document ingestion/retrieval/generation components.

### Key Resume Points

* Developed an end-to-end **RAG pipeline** covering PDF parsing, sentence-based chunking, embedding generation, vector indexing, semantic retrieval, and LLM response generation.
* Implemented **Elasticsearch dense-vector search with cosine similarity** to retrieve relevant document chunks for user queries.
* Added **token-aware context construction and embedding input truncation** to manage LLM and embedding model constraints.
* Designed a modular Python architecture separating **parsing, chunking, embedding, indexing, retrieval, and generation** responsibilities.
* Implemented **exponential-backoff retries and structured logging** for improved API reliability and debugging.
