import streamlit as st
import pandas as pd
import time
from datetime import datetime
from random import randint
import plotly.express as px
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector_db import get_retriever   # ✅ FIXED IMPORT

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Warehouse AI Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# GLOBAL CSS
# ==================================================
st.markdown("""
<style>
.stApp {
    background: #000000;
    color: #ffffff;
}
.chat-bubble {
    background: #0d0d0d;
    padding: 12px;
    border-radius: 12px;
    border-left: 4px solid #00ffd5;
    margin-bottom: 10px;
}
.kpi-card {
    background: #1a1a1a;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.title("🏭 Warehouse AI Assistant Dashboard")
datetime_box = st.empty()
datetime_box.write(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ==================================================
# SESSION STATE
# ==================================================
st.session_state.setdefault("messages", [])
st.session_state.setdefault("activity_log", [])
st.session_state.setdefault("uploaded_inventory", None)
st.session_state.setdefault("assistant_mode", "Inventory")

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.header("⚙️ Controls")

    st.session_state.assistant_mode = st.selectbox(
        "Assistant Mode", ["Inventory", "Shipment", "Multi-Task"]
    )

    file = st.file_uploader("Upload Inventory (CSV/Excel)", type=["csv", "xlsx"])
    if file:
        try:
            df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
            st.session_state.uploaded_inventory = df
            st.success("Inventory uploaded.")
        except Exception as e:
            st.error(f"Upload failed: {e}")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🔄 Refresh"):
        st.cache_resource.clear()
        st.rerun()

# ==================================================
# KPI ROW
# ==================================================
col1, col2, col3 = st.columns(3)
col1.metric("Total Inventory", randint(5000, 10000))
col2.metric("Shipments", randint(100, 500))
col3.metric("SKU Count", randint(40, 140))

st.divider()

# ==================================================
# PREVIEW INVENTORY
# ==================================================
if st.session_state.uploaded_inventory is not None:
    df = st.session_state.uploaded_inventory
    st.subheader("📊 Inventory Preview")
    st.dataframe(df.head(), use_container_width=True)

    if "Category" in df.columns:
        fig = px.pie(df, names="Category", title="Category Breakdown")
        st.plotly_chart(fig, use_container_width=True)

# ==================================================
# LOAD RETRIEVER + AI CHAIN
# ==================================================
@st.cache_resource
def load_retriever_cached():
    return get_retriever()

retriever = load_retriever_cached()

@st.cache_resource
def load_chain():
    model = OllamaLLM(model="gemma3:latest")

    template = """
You are a warehouse AI assistant.

Mode: {mode}
Rules:
- Use ONLY inventory data provided
- If data is missing, reply: "Data not available."
- Be concise and factual.

Records:
{records}

Question:
{question}

Provide an accurate answer.
"""
    return ChatPromptTemplate.from_template(template) | model

chain = load_chain()

# ==================================================
# CHAT
# ==================================================
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(f"<div class='chat-bubble'>{m['content']}</div>", unsafe_allow_html=True)

query = st.chat_input("Ask a warehouse question...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                docs = retriever.invoke(query)
                records = "\n".join(d.page_content for d in docs) if docs else ""

                response = chain.invoke({
                    "records": records,
                    "question": query,
                    "mode": st.session_state.assistant_mode
                })

            except Exception as e:
                response = f"Error: {e}"

            st.markdown(f"<div class='chat-bubble'>{response}</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ==================================================
# FOOTER
# ==================================================
st.caption("Warehouse AI • Powered by Chroma + Ollama + Streamlit")
