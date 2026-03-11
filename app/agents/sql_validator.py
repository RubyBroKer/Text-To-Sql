from typing import TypedDict

from validators.sql_rules import validate_sql_rules


class GraphState(TypedDict):

    sql_query: str
    sql_valid: bool
    validation_error: str


def sql_validator_agent(state: GraphState):

    sql_query = state["sql_query"]

    valid, error = validate_sql_rules(sql_query)

    if not valid:
        return {
            "sql_valid": False,
            "validation_error": error
        }

    return {
        "sql_valid": True,
        "validation_error": None
    }