# 🧠 Natural Language SQL Query Assistant edited by 002 and 003
### Query Postgres using English. Powered by Azure OpenAI + Streamlit + PandasAI.

---

## 📌 Overview

This project provides a **conversational analytics interface** that enables business users to query a PostgreSQL database using **plain English**, without writing SQL.  
The system:

✅ Converts natural-language questions → **SQL** (via Azure OpenAI)  
✅ Enforces **strict SQL safety guardrails**  
✅ Executes queries in **read-only mode** against Postgres  
✅ Displays results in a clean **Streamlit UI**  
✅ Allows follow-up analysis using **PandasAI** (“Chat with your DataFrame”)  

It eliminates the dependency on data engineers for ad-hoc analytics while maintaining strong data governance.

---

## 🚀 Features

### 💬 Natural Language → SQL
- GPT-4o mini (Azure OpenAI) generates SQL from English questions
- Schema-aware prompt: database structure is dynamically injected
- Output is cleaned (no markdown, backticks, or multiple statements)

### 🔐 SQL Safety Guardrails
- SELECT-only enforcement  
- Single-statement detection  
- Forbidden keyword blocklist (`DROP`, `ALTER`, `UPDATE`, etc.)  
- Automatic `LIMIT` injection  
- Read-only execution in Postgres  

### 📊 Self-Service Analytics (PandasAI)
- Users can ask questions of the returned DataFrame:
  - “Summarize this”
  - “Plot number of aircraft by status”
  - “Find anomalies”
- Supports text output, tables, and visualizations

### 🖥️ Modern Streamlit Interface
- Interactive, user-friendly UI
- History maintained with `st.session_state`
- Form-based PandasAI input to prevent page resets on pressing Enter

### ⚙️ Clean Engineering
- Fully modular Python architecture  
- Poetry environment & dependency management  
- Pydantic-based configuration  
- Unit tests for SQL guardrails and LLM environment setup  

---

# 🏗️ Architecture
app/
main.py # Streamlit UI orchestrator
utilities/
config.py # Azure + Postgres settings via pydantic-settings
llm.py # AzureOpenAI client factory
generator.py # NL → SQL generation (with cleanup)
validator.py # SQL guardrails (SELECT-only, blocklists, etc.)
sql_executor.py # Safe read-only query execution
pandasai_integration.py # Chat-with-DataFrame functionality


---

## ✅ System Design Diagram

```mermaid
flowchart TB

user([Business User]) --> UI

subgraph UI[Streamlit Front-End]
    Q[Ask Question]
    Gen[[Generate SQL]]
    Run[[Run SQL]]
    Pandas[[Analyze with PandasAI]]
end

Q --> Gen --> DisplaySQL[Show SQL]
DisplaySQL --> Run --> DF[Render DataFrame]
DF --> Pandas --> Analysis[Text/Table/Plot]

subgraph LLM[Azure OpenAI]
    Prompt[Prompt + Schema]
    GPT[GPT-4o Mini<br/>Chat Completions]
    Clean[Clean SQL Output]
end

Prompt --> GPT --> Clean

subgraph Guard[SQL Validator]
    Single[Single Statement]
    SelectOnly[SELECT-Only]
    Blocked[Keyword Blocklist]
    Limit[Force LIMIT]
end

Clean --> Single --> SelectOnly --> Blocked --> Limit

subgraph DB[(PostgreSQL)]
    Tables[(User Tables)]
end

Limit --> Exec[Execute Read-Only SQL] --> DB
Exec --> DF

subgraph PandasAI
    PrepEnv[Prepare Azure Env]
    SmartDF[SmartDataframe.chat()]
end

DF --> PrepEnv --> SmartDF --> Analysis

