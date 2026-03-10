from pydantic import BaseModel, Field
from typing import Optional, List


class Task(BaseModel):

    task_name: str = Field(
        description="Short identifier for the task"
    )

    intent: str = Field(
        description="Type of analysis such as aggregation, trend_analysis, comparison, distribution, correlation, forecast, general_query"
    )

    metric: Optional[str] = Field(
        default=None,
        description="Numerical column being analyzed"
    )

    dimension: Optional[str] = Field(
        default=None,
        description="Column used for grouping"
    )

    filters: Optional[str] = Field(
        default=None,
        description="Filtering conditions like date ranges or city"
    )

    top_n: Optional[int] = Field(
        default=None,
        description="Top N results requested"
    )

    visualization: str = Field(
        description="Suggested visualization type"
    )


class TaskList(BaseModel):

    tasks: List[Task]