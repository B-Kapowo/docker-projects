from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import PGVector
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
import os

# --- 1. Set up your tools ---
# SQL Database Tool
db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:Welcometosangiro%40123@localhost:5432/company_db")
sql_toolkit = SQLDatabaseToolkit(db=db, llm=Ollama(model="gemma", base_url="http://localhost:11434"))
sql_tools = sql_toolkit.get_tools()

# RAG Tool
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
db_vector = PGVector(embedding_function=embeddings, collection_name="employees", connection_string="postgresql+psycopg2://postgres:Welcometosangiro%40123@localhost:5432/company_db")
retriever = db_vector.as_retriever()
rag_chain = RetrievalQA.from_chain_type(llm=Ollama(model="gemma", base_url="http://localhost:11434"), retriever=retriever)
rag_tool = Tool(
    name="RAG Tool",
    func=rag_chain.run,
    description="Useful for general knowledge questions about the data."
)

# Combine all tools
all_tools = sql_tools + [rag_tool]

# --- 2. Create the hybrid agent ---
# Define the agent's prompt
prompt = PromptTemplate.from_template("""
You are an AI assistant with access to two tools:
1. SQL Tool: Use this for structured queries, counting, filtering, and aggregation.
2. RAG Tool: Use this for general questions about the data.
Based on the user's input, choose the most appropriate tool to provide a detailed response.

Question: {input}
""")

agent = create_react_agent(llm=Ollama(model="gemma", base_url="http://localhost:11434"), tools=all_tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)

# Example Queries
# This will use the SQL Tool
agent_executor.run("How many employees are there?") 
# This will use the RAG Tool
agent_executor.run("What is the role of a Project Manager?")