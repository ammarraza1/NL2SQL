import os
from utilities.pandasai_integration import _prepare_openai_env_for_azure

def test_prepare_openai_env_for_azure_sets_envs(monkeypatch):
    # clear first
    for k in ["OPENAI_API_TYPE","OPENAI_API_KEY","OPENAI_API_BASE","OPENAI_API_VERSION",
              "AZURE_OPENAI_API_KEY","AZURE_OPENAI_ENDPOINT","AZURE_OPENAI_API_VERSION"]:
        monkeypatch.delenv(k, raising=False)

    _prepare_openai_env_for_azure(
        api_key="KEY",
        endpoint="https://myres.openai.azure.com/",
        api_version="2024-10-21",
    )

    assert os.environ["OPENAI_API_TYPE"] == "azure"
    assert os.environ["OPENAI_API_KEY"] == "KEY"
    assert os.environ["OPENAI_API_BASE"] == "https://myres.openai.azure.com"
    assert os.environ["OPENAI_API_VERSION"] == "2024-10-21"
    assert os.environ["AZURE_OPENAI_API_KEY"] == "KEY"
    assert os.environ["AZURE_OPENAI_ENDPOINT"] == "https://myres.openai.azure.com"
    assert os.environ["AZURE_OPENAI_API_VERSION"] == "2024-10-21"
