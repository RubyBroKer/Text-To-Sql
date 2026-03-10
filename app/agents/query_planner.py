import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from typing import TypedDict, List, Dict, Any

from schemas.query_plan_schema import QueryPlanList

class GraphState(TypedDict):
    question: str
    tasks: List[Dict[str, Any]]
    query_plans: List[Dict[str, Any]]

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
You are a query planning agent for a data analytics system.

Your job is to convert analytical tasks into database query plans.

Database schema:

{DATABASE_SCHEMA}

Rules:

1. Use only tables and columns from the schema.
2. Decide which tables are needed.
3. Identify columns required.
4. Determine grouping, filtering and ordering logic.
5. Extract limits when tasks ask for top N.

Return a structured query plan.
"""


# -------------------------
# LLM
# -------------------------

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY")
)

planner_agent = create_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    response_format=QueryPlanList
)


# -------------------------
# LangGraph Node
# -------------------------

def query_planner_node(state: GraphState):

    tasks = state["tasks"]

    result = planner_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"Generate query plans for the following tasks:\n{tasks}"
            }
        ]
    })

    plans = result["structured_response"]

    return {
        "query_plans": [p.model_dump() for p in plans.query_plans]
    }