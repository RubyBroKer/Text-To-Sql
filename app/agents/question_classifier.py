from pydantic import BaseModel, Field
from typing import Optional, List
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
from typing import TypedDict, List, Dict, Any
from schemas.task_schema import TaskList
from langchain_groq import ChatGroq
from langchain.agents import create_agent


class GraphState(TypedDict):

    question: str
    tasks: List[Dict[str, Any]]


SYSTEM_PROMPT = """
You are a data analytics query classifier.

Your job is to convert a user's natural language question into structured analytical tasks.

The dataset represents a ride-sharing platform similar to Uber.

Rules:

1. Break the question into one or more tasks.
2. Each task represents one dataset, chart, or analysis.
3. If the question asks multiple things, create multiple tasks.
4. If metric or dimension is unclear, set it to null.

Intent types:

aggregation
trend_analysis
comparison
distribution
correlation
forecast
general_query

Visualization mapping:

trend_analysis -> line_chart
aggregation -> bar_chart
comparison -> bar_chart
distribution -> histogram
correlation -> scatter_plot
forecast -> line_chart
general_query -> table
"""


llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY")
)


classifier_agent = create_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    response_format=TaskList
)

def question_classifier_node(state: GraphState):

    question = state["question"]

    result = classifier_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })

    tasks = result["structured_response"]

    return {
        "tasks": [task.model_dump() for task in tasks.tasks]
    }