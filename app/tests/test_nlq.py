import os
import pytest
from app.utilities.config import settings
from app.utilities.db.engine import get_engine
from app.utilities.llm import get_pandasai_llm

def test_engine_constructs():
    # Just ensure engine can be built from env vars
    engine = get_engine()
    assert engine is not None

@pytest.mark.skipif(
    not (settings.AZURE_OPENAI_API_KEY and settings.AZURE_OPENAI_ENDPOINT and settings.AZURE_OPENAI_DEPLOYMENT),
    reason="Azure OpenAI not configured in test environment",
)
def test_llm_constructs():
    llm = get_pandasai_llm()
    assert llm is not None
