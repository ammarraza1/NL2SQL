import streamlit as st
import pandas as pd
from utilities.config import get_settings
from utilities.db.engine import ping, read_only_conn
from sqlalchemy import text
from utilities.db.schema import get_schema_snippet
from utilities.generator import draft_sql
from utilities.sql_executor import execute_safe_sql
from utilities.pandasai_integration import analyze_with_pandasai
from utilities.config import get_settings

st.set_page_config(page_title="NL→SQL Assistant", layout="wide")

def _init_state():
    st.session_state.setdefault("schema_snippet", "")
    st.session_state.setdefault("latest_sql", "")
    st.session_state.setdefault("latest_df", None)          # holds the last query result DataFrame
    st.session_state.setdefault("analysis_q", "")
    st.session_state.setdefault("analysis_result", None)     # text/df/plot result from PandasAI

_init_state()

st.title("🧠 Natural Language → SQL (Postgres)")

if "analysis_result" in st.session_state:
    st.info("Previous PandasAI result:")
    result = st.session_state["analysis_result"]
    if isinstance(result, pd.DataFrame):
        st.dataframe(result)
    else:
        st.write(result)

s = get_settings()

with st.sidebar:
    st.header("Connection")
    st.write(f"DB: {s.pg_user}@{s.pg_host}:{s.pg_port}/{s.pg_database}")
    if st.button("Test DB connection"):
        ok = ping()
        st.success("Connected!") if ok else st.error("Connection failed. Check .env.")

st.subheader("Ask your database in natural language")

question = st.text_area("Your question:", placeholder="e.g., show me top 10 customers by revenue last month")
if st.button("Generate SQL"):
    with st.spinner("Reflecting schema..."):
        schema_snippet = get_schema_snippet()
        print(f"schema_snippet: {schema_snippet}")
    with st.spinner("Generating SQL..."):
        try:
            sql = draft_sql(question, schema_snippet)
            st.code(sql, language="sql")
            st.session_state["latest_sql"] = sql
        except Exception as e:
            st.error(f"Error generating SQL: {e}")

if st.button("Run Generated SQL", key="btn_run_sql"):
    sql_gen = st.session_state.get("latest_sql")
    if not sql_gen:
        st.warning("Generate SQL first.")
    else:
        try:
            with st.spinner("Executing query..."):
                df_exec = execute_safe_sql(sql_gen, s.default_row_limit)
            st.session_state["latest_df"] = df_exec           # <- persist across reruns
            st.session_state["analysis_result"] = None         # reset old analysis when new data arrives
            st.success(f"Returned {len(df_exec)} rows")
            st.dataframe(df_exec)
        except Exception as e:
            st.error(f"Error executing SQL: {e}")

            # PandasAI panel (only when df exists)
            st.markdown("---")
            st.subheader("Analyze results with PandasAI (optional)")

            with st.form("pandasai_form", clear_on_submit=False):
                analysis_q = st.text_input(
                    "Ask about the result DataFrame (e.g., 'summarize it', 'plot count by status')",
                    key="analysis_q",
                    help="Press Enter or click the button to analyze with PandasAI."
                )
                submitted = st.form_submit_button("Analyze with PandasAI")

            if submitted:
                df_latest = st.session_state.get("latest_df")
                if df_latest is not None:
                    st.markdown("---")
                    st.subheader("Analyze results with PandasAI (optional)")

                    with st.form("pandasai_form", clear_on_submit=False):
                        analysis_q_val = st.text_input(
                            "Ask about the result DataFrame (e.g., 'summarize it', 'plot count by status')",
                            key="analysis_q",
                            help="Press Enter or click to analyze. The result persists across reruns."
                        )
                        submitted = st.form_submit_button("Analyze with PandasAI", use_container_width=True)

                    if submitted:
                        if not analysis_q_val.strip():
                            st.warning("Enter a question first.")
                        else:
                            try:
                                with st.spinner("Thinking with PandasAI..."):
                                    result = analyze_with_pandasai(df_latest, analysis_q_val)
                                st.session_state["analysis_result"] = result   # <- persist the analysis output
                                st.success("PandasAI response saved below.")
                            except Exception as e:
                                st.error(f"PandasAI error: {e}")

                    # Always show the last analysis result if we have one
                    if st.session_state.get("analysis_result") is not None:
                        st.subheader("PandasAI Result")
                        res = st.session_state["analysis_result"]
                        import pandas as pd
                        if isinstance(res, pd.DataFrame):
                            st.dataframe(res)
                        else:
                            st.write(res)

        except Exception as e:
            st.error(f"Error executing SQL: {e}")