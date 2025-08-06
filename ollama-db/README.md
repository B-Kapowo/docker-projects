Custom Local LLM for Database Querying

This guide outlines three different approaches for building a custom local Large Language Model (LLM) that can query data residing in a local PostgreSQL or Baserow database. Each approach is suited for a different type of query, and a final "hybrid" solution is presented to combine their strengths.

## 1. The SQL Agent Approach

This method is ideal for **structured, aggregate, and filtered queries** where data is well-organized in a database table. The LLM generates and executes a precise SQL query to get an exact answer.

### Key Components
* **Database:** PostgreSQL.
* **Local LLM:** Ollama (e.g., `gemma`).
* **Framework:** LangChain with its `SQLDatabaseToolkit`.

### How It Works
1.  The user asks a question like "How many users logged into server X today?"
2.  The LangChain SQL Agent, powered by the LLM, analyzes the database schema.
3.  The LLM generates a SQL query (e.g., `SELECT COUNT(session_id) FROM sessions WHERE server_hostname = 'X' AND login_date = CURRENT_DATE;`).
4.  The query is executed against the PostgreSQL database.
5.  The results are returned to the user.

### How to Run

1.  **Set up the database and ingest data:**
    ```bash
    python3 ingest_data.py
    ```

2.  **Run the SQL agent:**
    ```bash
    python3 sql_agent.py
    ```

## 2. The RAG (Retrieval-Augmented Generation) Approach
This method is best for answering semantic or open-ended questions about unstructured text data. The LLM retrieves relevant data chunks and uses them as context to formulate a response. This is also the best approach for integer-oriented data, as long as it is first transformed into descriptive text.

### Key Components
* **Database:** PostgreSQL with the pgvector extension.
* **Local LLM:** Ollama (for both embedding and generation models).
* **Framework:** LangChain (for data ingestion, chunking, and the RAG chain).
* **Data Processing:** Pandas (for handling CSV data).

### How It Works
1.  **Ingestion:** Data from a CSV is loaded and transformed into descriptive, natural language text.
2.  **Embedding:** The text is split into chunks, and each chunk is converted into a numerical vector (embedding).
3.  **Storage:** The embeddings are stored in PostgreSQL using pgvector.
4.  **Retrieval:** The user's query is also embedded, and the most semantically similar data chunks are retrieved from the database.
5.  **Generation:** These retrieved chunks are provided as context to the LLM, which then generates a detailed answer.

## 3. The Hybrid RAG + SQL Agent Approach
This is the most powerful and flexible solution. An intelligent LLM agent is given access to both a SQL tool and a RAG tool, allowing it to intelligently choose the best method for any given query. This is the recommended approach for handling a wide variety of queries.

### Key Components
* All components from both the SQL Agent and RAG approaches.
* An LLM agent that can orchestrate multiple tools.

### How It Works
1.  The user asks a question.
2.  A master LLM agent analyzes the query.
3.  If the query requires aggregation or filtering: The agent chooses the SQL Tool, generates a SQL query, and executes it.
4.  If the query is a simple lookup or semantic question: The agent chooses the RAG Tool, performs a vector search, and uses the retrieved context to answer.
5.  The agent synthesizes the final response and presents it to the user.

### How to Run

1.  **Set up the database and ingest data:**
    ```bash
    python3 ingest_data.py
    ```

2.  **Run the hybrid agent:**
    ```bash
    python3 hybrid_agent.py
    ```