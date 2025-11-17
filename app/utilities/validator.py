from __future__ import annotations
import re
import sqlparse

_BLOCKLIST = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|GRANT|REVOKE|CREATE|MERGE)\b", re.I)

def is_single_statement(sql: str) -> bool:
    stmts = [s for s in sqlparse.parse(sql) if s.tokens]
    return len(stmts) == 1

def is_select_only(sql: str) -> bool:
    parsed = sqlparse.parse(sql)
    if not parsed:
        return False
    return parsed[0].get_type().upper() == "SELECT"

def contains_blocked_keywords(sql: str) -> bool:
    return bool(_BLOCKLIST.search(sql))

def ensure_limit(sql: str, row_limit: int) -> str:
    # naive but effective: add LIMIT if none present (ignoring subqueries here)
    if re.search(r"\bLIMIT\s+\d+\b", sql, flags=re.I):
        return sql
    return f"{sql.rstrip(';')} LIMIT {row_limit}"
