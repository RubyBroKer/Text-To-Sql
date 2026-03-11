from langgraph.graph import StateGraph, END

from graph.state import GraphState

from agents.question_classifier import question_classifier_node
from agents.query_planner import query_planner_node
from agents.sql_generator import sql_generator_node
from agents.sql_validator import sql_validator_agent


def build_graph():

    builder = StateGraph(GraphState)

    # Nodes
    builder.add_node(
        "question_classifier",
        question_classifier_node
    )

    builder.add_node(
        "query_planner",
        query_planner_node
    )

    builder.add_node(
        "sql_generator",
        sql_generator_node
    )

    builder.add_node(
        "sql_validator",
        sql_validator_agent
    )

    # Entry point
    builder.set_entry_point("question_classifier")

    # Edges
    builder.add_edge(
        "question_classifier",
        "query_planner"
    )

    builder.add_edge(
        "query_planner",
        "sql_generator"
    )

    builder.add_edge(
        "sql_generator",
        "sql_validator"
    )

    builder.add_edge(
        "sql_validator",
        END
    )

    graph = builder.compile()

    return graph