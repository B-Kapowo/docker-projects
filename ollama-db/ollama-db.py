from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor, create_sql_agent
from langchain.agents.agent_types import AgentType
import os

# 1. Initialize Ollama LLM
# Ensure Ollama server is running (it usually starts automatically after installation)
llm = Ollama(model="gemma") # Or "gemma:7b" for a specific size

# 2. Connect to your PostgreSQL database
# Replace with your actual database credentials and host
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/mydb"
db = SQLDatabase.from_uri(DATABASE_URL)

# 3. Create a SQL Agent with LangChain
# This agent is designed to interact with SQL databases
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True, # Set to True to see the agent's thought process
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # A common agent type for this
)

# 4. Interact with the LLM to query your database
def query_database_with_llm(question):
    print(f"\nUser: {question}")
    response = agent_executor.run(question)
    print(f"\nLLM Response:\n{response}")
    return response

if __name__ == "__main__":
    # Example queries
    query_database_with_llm("How many users are in the 'users' table?")
    query_database_with_llm("Show me the names of the top 5 products by price from the 'products' table.")
    query_database_with_llm("What is the average order total in the 'orders' table?")

    # You can integrate this with a Streamlit UI or a simple command-line loop