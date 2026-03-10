from pydantic import BaseModel, Field
from typing import List


class SQLQuery(BaseModel):

    task_name: str = Field(description="Task identifier")

    sql: str = Field(description="Generated SQL query")


class SQLQueryList(BaseModel):

    sql_queries: List[SQLQuery]