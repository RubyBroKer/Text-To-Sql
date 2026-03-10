import os
from typing import TypedDict, List, Dict, Any

from langchain_groq import ChatGroq
from langchain.agents import create_agent

from schemas.sql_schema import SQLQuery


# -------------------------
# Graph State
# -------------------------

class GraphState(TypedDict):

    question: str
    tasks: List[Dict[str, Any]]
    query_plans: List[Dict[str, Any]]
    sql_queries: List[Dict[str, Any]]


# -------------------------
# Database Schema
# -------------------------

DATABASE_SCHEMA = """
Database: Uber-like ride sharing dataset

Tables:

trips
- trip_id
- driver_id
- rider_id
- pickup_time
- dropoff_time
- pickup_location
- dropoff_location
- distance
- fare_amount

drivers
- driver_id
- driver_name
- city
- rating

riders
- rider_id
- rider_name
- city
"""


# -------------------------
# System Prompt
# -------------------------

SYSTEM_PROMPT = f"""
You are a SQL generation agent.

Your job is to convert a query plan into a SQL query.

Database schema:

{DATABASE_SCHEMA}

Rules:

1. Use ONLY tables and columns from the schema
2. Follow the query plan strictly
3. Generate valid SQL
4. Apply grouping, filtering, ordering, and limits correctly
"""


# -------------------------
# LLM
# -------------------------

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY")
)

sql_agent = create_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    response_format=SQLQuery
)


# -------------------------
# LangGraph Node
# -------------------------

def sql_generator_node(state: GraphState):

    query_plans = state["query_plans"]

    sql_queries = []

    for plan in query_plans:

        result = sql_agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": f"Generate SQL for this query plan:\n{plan}"
                }
            ]
        })

        sql = result["structured_response"]

        sql_queries.append(sql.model_dump())

    return {
        "sql_queries": sql_queries
    }