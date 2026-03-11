import re

FORBIDDEN_KEYWORDS = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "grant",
    "revoke",
    "copy"
]

FORBIDDEN_TABLES = [
    "pg_catalog",
    "information_schema"
]


def validate_sql_rules(sql: str):

    sql_lower = sql.lower().strip()

    # block multiple statements
    if ";" in sql_lower[:-1]:
        return False, "Multiple SQL statements are not allowed"

    # allow only select queries
    if not sql_lower.startswith("select"):
        return False, "Only SELECT queries are allowed"

    # forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql_lower):
            return False, f"Forbidden keyword detected: {keyword}"

    # system tables
    for table in FORBIDDEN_TABLES:
        if table in sql_lower:
            return False, f"Access to system table blocked: {table}"

    return True, None