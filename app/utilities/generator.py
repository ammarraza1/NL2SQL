from __future__ import annotations
from utilities.llm import get_azure_client, get_deployment_name
from utilities.config import get_settings
from utilities.prompt import SYSTEM_PROMPT, USER_TEMPLATE

def draft_sql(question: str, schema_snippet: str) -> str:
    s = get_settings()
    client = get_azure_client()
    deployment = get_deployment_name()

    user_msg = USER_TEMPLATE.format(
        schema=schema_snippet,
        row_limit=s.default_row_limit,
        question=question.strip(),
    )
    print(f"user_msg: {user_msg}")

    resp = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.0,
    )
    print(f"resp: {resp}")
    sql = (resp.choices[0].message.content or "").strip()
    return sql
