# app/utilities/llm.py
from __future__ import annotations
from openai import AzureOpenAI
from utilities.config import get_settings

_client: AzureOpenAI | None = None

def get_azure_client() -> AzureOpenAI:
    global _client
    if _client is None:
        s = get_settings()
        _client = AzureOpenAI(
            api_key=s.azure_openai_api_key,
            api_version=s.azure_openai_api_version,
            azure_endpoint=s.azure_openai_endpoint,
        )
    return _client

def get_deployment_name() -> str:
    return get_settings().azure_openai_deployment
