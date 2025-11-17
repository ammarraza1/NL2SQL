from typing import Optional
import pandas as pd
from sqlalchemy import text
from pandasai import SmartDataframe

from .db.engine import get_engine
from .llm import get_pandasai_llm

def load_table_df(table: str, schema: str = "public", limit: int = 5000) -> pd.DataFrame:
    """
    Load a table into a DataFrame with a LIMIT for safety.
    """
    engine = get_engine()
    query = text(f'SELECT * FROM "{schema}"."{table}" LIMIT :limit')
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"limit": limit})
    return df

def ask_dataframe(df: pd.DataFrame, question: str) -> str:
    """
    Ask a natural-language question against a pandas DataFrame using pandasai.
    """
    llm = get_pandasai_llm()
    sdf = SmartDataframe(
        df,
        config={
            "llm": llm,
            # keep output textual for now; we'll add charts/downloads later
            "save_logs": False,
            "enforce_privacy": False,
        },
    )
    # sdf.chat returns text; if it generates a plot, pandasai may also display it.
    return str(sdf.chat(question))

def ask_table(question: str, table: str, schema: str = "public", limit: int = 5000) -> str:
    df = load_table_df(table=table, schema=schema, limit=limit)
    return ask_dataframe(df, question)
