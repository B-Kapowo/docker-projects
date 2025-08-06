from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
import os

# 1. Initialize Ollama LLM
# Ensure Ollama server is running (it usually starts automatically after installation)
from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="gemma", base_url="http://localhost:11434") # Or "gemma:7b" for a specific size

# 2. Connect to your PostgreSQL database
# Replace with your actual database credentials and host
DATABASE_URL = "postgresql+psycopg2://postgres:Welcometosangiro%40123@localhost:5432/company_db"
db = SQLDatabase.from_uri(DATABASE_URL)

# 3. Create a SQL Agent with LangChain
# This agent is designed to interact with SQL databases
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True, # Set to True to see the agent's thought process
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # A common agent type for this
    handle_parsing_errors=True,
)

# 4. Interact with the LLM to query your database
def query_database_with_llm(question):
    print(f"\nUser: {question}")
    response = agent_executor.invoke({"input": question})
    print(f"\nLLM Response:\n{response}")
    return response

if __name__ == "__main__":
    # Example queries
    query_database_with_llm("How many employees are in the 'employees' table?")
    query_database_with_llm("Show me the names of the top 3 employees by salary from the 'employees' table.")
    query_database_with_llm("What is the average salary in the 'employees' table?")

    # You can integrate this with a Streamlit UI or a simple command-line loop