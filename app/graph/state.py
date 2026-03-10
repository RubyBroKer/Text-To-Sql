from typing import TypedDict, List, Dict, Any


class GraphState(TypedDict):

    question: str

    tasks: List[Dict[str, Any]]

    query_plans: List[Dict[str, Any]]

    sql_queries: List[Dict[str, Any]]

    datasets: List[Any]