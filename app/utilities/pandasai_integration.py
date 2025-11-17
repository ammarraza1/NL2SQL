# app/utilities/pandasai_integration.py
from __future__ import annotations
import os
import typing as t
import pandas as pd

def _prepare_openai_env_for_azure(
    *,
    api_key: str,
    endpoint: str,
    api_version: str,
) -> None:
    """
    Configure environment variables so libraries that depend on the OpenAI SDK
    (like PandasAI) can use Azure OpenAI transparently.
    """
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_KEY"] = api_key
    # PandasAI / OpenAI SDK expects BASE without trailing paths
    os.environ["OPENAI_API_BASE"] = endpoint.rstrip("/")
    os.environ["OPENAI_API_VERSION"] = api_version
    # Some tools look for these Azure-specific keys too:
    os.environ["AZURE_OPENAI_API_KEY"] = api_key
    os.environ["AZURE_OPENAI_ENDPOINT"] = endpoint.rstrip("/")
    os.environ["AZURE_OPENAI_API_VERSION"] = api_version

def analyze_with_pandasai(
    df: pd.DataFrame,
    question: str,
    *,
    azure_api_key: str,
    azure_endpoint: str,
    azure_api_version: str,
) -> t.Any:
    """
    Run a natural-language analysis on a DataFrame via PandasAI.

    Returns whatever PandasAI returns:
    - A scalar / small table as text
    - A new DataFrame
    - A matplotlib figure (PandasAI may also display it)
    """
    if df is None or df.empty:
        raise ValueError("No data to analyze.")

    # Late import so the app runs even if pandasai isn't installed (or optional)
    try:
        from pandasai import SmartDataframe
    except Exception as e:
        raise ImportError(
            "pandasai is not available. Make sure it is installed in your Poetry env."
        ) from e

    _prepare_openai_env_for_azure(
        api_key=azure_api_key,
        endpoint=azure_endpoint,
        api_version=azure_api_version,
    )

    # Keep config simple; you can add output parsers or enable logs later
    sdf = SmartDataframe(df, config={"verbose": False})
    # Common examples: "summarize this", "plot sales by month", etc.
    return sdf.chat(question.strip())
