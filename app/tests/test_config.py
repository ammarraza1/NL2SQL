from utilities.config import get_settings

def test_settings_loads():
    s = get_settings()
    assert s.azure_openai_endpoint
    assert s.pg_host
