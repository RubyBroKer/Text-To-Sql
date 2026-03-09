from groq import Groq
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from dataclasses import dataclass
from pydantic import BaseModel, Field
import psycopg2
from langchain.tools import tool

from langchain.tools import tool
import psycopg2
import os

@tool
def execute_sql_query(sql: str) -> str:
    """
    Executes a SQL query on the PostgreSQL database and only return the results.Don't give any explanation of data or anything.I need to store this data in persistent memory
    """

    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = conn.cursor()
        sql = sql.replace("```sql", "").replace("```", "").strip()
        cursor.execute(sql)

        # If SELECT query
        if cursor.description:
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            results = [dict(zip(columns, row)) for row in rows]

            conn.close()
            return str(results)

        conn.commit()
        conn.close()

        return "Query executed successfully."

    except Exception as e:
        return f"SQL execution error: {str(e)}"
    
SYSTEM_PROMPT = """
You are an expert SQL assistant.

Your job is to answer user questions by generating SQL queries and executing them.

Database Schema:

Table: users
columns:
 id           | uuid
 name         | character varying
 email        | character varying
 phone_number | character varying
 role         | character varying
 is_active    | boolean
 created_at   | timestamp

Rules:
1. Convert the user question into a SQL query.
2. Use the execute_sql_query tool to run the query.
3. Return the results from the tool.

Important:
- Use only tables and columns from the schema.
- Do not hallucinate tables or columns.
- If the request cannot be answered, say "Unable to generate SQL".
"""

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY")
)

agent = create_agent(
    model=llm,
    tools=[execute_sql_query],
    system_prompt=SYSTEM_PROMPT
)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "give me the sql query to fetch all the users from the users table"
            }
        ]
    }
)

print(response["messages"][-1].content)