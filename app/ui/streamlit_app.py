import streamlit as st
from app.utilities.nlq import ask_table, load_table_df
from app.utilities.db.engine import get_engine

st.set_page_config(page_title="NLQ → SQL (pandasAI + Azure OpenAI)", layout="wide")
st.title("NLQ → SQL (pandasAI + Azure OpenAI)")

with st.sidebar:
    st.subheader("Data source (Postgres)")
    schema = st.text_input("Schema", value="public")
    table = st.text_input("Table", value="")
    row_limit = st.number_input("Row limit (preview + LLM)", min_value=100, max_value=200000, value=5000, step=100)
    st.caption("Tip: start with a small table while testing.")

    st.subheader("Utilities")
    if st.button("Test DB connection"):
        try:
            engine = get_engine()
            with engine.connect() as conn:
                conn.execute(st.experimental_connection("noop", type="noop"))  # no-op, just ensure connect works
            st.success("Connected to Postgres successfully.")
        except Exception as e:
            st.error(f"Postgres connection failed: {e}")

st.write("### 1) Preview data (optional)")
col1, col2 = st.columns([2,1])
with col1:
    if st.button("Load preview", use_container_width=True, type="secondary"):
        if not table:
            st.warning("Please enter a table name.")
        else:
            try:
                df = load_table_df(table=table, schema=schema, limit=row_limit)
                st.dataframe(df.head(50), use_container_width=True)
                st.success(f"Loaded {min(len(df), row_limit)} rows from {schema}.{table}")
            except Exception as e:
                st.error(f"Failed to load table: {e}")

st.write("### 2) Ask a question")
question = st.text_input(
    "Natural-language question about the selected table",
    placeholder='e.g., "What is the average order amount by month?"',
)

run = st.button("Run", type="primary")
if run:
    if not table:
        st.warning("Please enter a table name first.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking with pandasai + Azure OpenAI..."):
            try:
                answer = ask_table(question=question, table=table, schema=schema, limit=row_limit)
                st.markdown("#### Answer")
                st.write(answer)
            except Exception as e:
                st.error(f"NLQ failed: {e}")

st.caption(
    "This prototype loads a table into a DataFrame and asks your question with pandasai using Azure OpenAI. "
    "Next, we’ll add safer SQL generation, multiple-table joins, auth/secrets handling, logging, and unit tests."
)
