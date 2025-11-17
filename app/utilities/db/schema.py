from __future__ import annotations
from sqlalchemy import inspect
from utilities.db.engine import get_engine

def get_schema_snippet(limit_tables: int = 10) -> str:
    """
    Reflects the current database schema (limited for prompt size)
    and returns a human-readable schema summary string.
    """
    engine = get_engine()
    insp = inspect(engine)
    schemas = insp.get_schema_names()
    print(f"schemas: {schemas}")
    out_lines: list[str] = []
    for schema in schemas:
        print(f"schema: {schema}")
        tables = insp.get_table_names(schema=schema)
        print(f"tables: {tables}")
        for t in tables[:limit_tables]:
            print(f"t: {t}")
            cols = [c["name"] for c in insp.get_columns(t, schema=schema)]
            print(f"cols: {cols}")
            out_lines.append(f"{schema}.{t}({', '.join(cols)})")
            print(f"out_lines: {out_lines}")
    return "\n".join(out_lines)
