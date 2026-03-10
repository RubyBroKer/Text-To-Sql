from pydantic import BaseModel, Field
from typing import List, Optional


class QueryPlan(BaseModel):

    task_name: str = Field(description="Task identifier")

    tables: List[str] = Field(
        description="Database tables required for the query"
    )

    columns: List[str] = Field(
        description="Columns needed from the tables"
    )

    operation: str = Field(
        description="Type of operation like aggregation, trend_analysis, comparison"
    )

    group_by: Optional[List[str]] = Field(
        default=None,
        description="Columns used for grouping"
    )

    filters: Optional[List[str]] = Field(
        default=None,
        description="Filtering conditions"
    )

    order_by: Optional[str] = Field(
        default=None,
        description="Sorting condition"
    )

    limit: Optional[int] = Field(
        default=None,
        description="Limit for top N results"
    )


class QueryPlanList(BaseModel):

    query_plans: List[QueryPlan]