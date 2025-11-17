from __future__ import annotations
import pandas as pd
from sqlalchemy import text
from utilities.db.engine import read_only_conn
from utilities.validator import (
    is_select_only,
    is_single_statement,
    contains_blocked_keywords,
    ensure_limit,
)

def execute_safe_sql(sql: str, row_limit: int = 200) -> pd.DataFrame:
    """
    Validate the SQL and execute it safely in read-only mode.
    """
    if not sql.strip():
        raise ValueError("Empty SQL.")
    if not is_single_statement(sql):
        raise ValueError("Only one SQL statement is allowed.")
    if not is_select_only(sql):
        raise ValueError("Only SELECT statements are allowed.")
    if contains_blocked_keywords(sql):
        raise ValueError("SQL contains forbidden keywords.")
    sql = ensure_limit(sql, row_limit)
    with read_only_conn() as conn:
        df = pd.read_sql(text(sql), conn)
    return df
