import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Personal Finance Agent", layout="wide")

# Backend URL
if "backend_url" not in st.session_state:
    st.session_state.backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

backend_url = st.text_input("Backend URL", value=st.session_state.backend_url)
st.session_state.backend_url = backend_url

st.title("💰 Personal Finance Agent")

tab_chat, tab_upload, tab_txns, tab_insights = st.tabs(["Chat", "Upload CSV", "Transactions", "Weekly Insights"])

# --- Chat Tab ---
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("Ask about your finances..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        try:
            resp = requests.post(
                f"{backend_url}/chat", json={"message": user_input}, timeout=30,
            )
            data = resp.json()
            reply = data["response"]
        except Exception as e:
            reply = f"Error contacting backend: {e}"

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

# --- Upload CSV Tab ---
with tab_upload:
    st.subheader("Upload Transactions CSV")
    uploaded = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded and st.button("Upload and Sync"):
        # Save to temp and sync
        with open("temp.csv", "wb") as f:
            f.write(uploaded.getvalue())
        try:
            resp = requests.post(
                f"{backend_url}/sync", json={"csv_path": "temp.csv"}, timeout=30,
            )
            st.success(resp.json()["message"])
        except Exception as e:
            st.error(f"Error: {e}")

# --- Transactions Tab ---
with tab_txns:
    st.subheader("Transaction History")
    if st.button("Load Transactions"):
        try:
            resp = requests.get(f"{backend_url}/transactions", timeout=10)
            txns = resp.json()
            if txns:
                df = pd.DataFrame(txns)
                st.dataframe(df)
            else:
                st.info("No transactions found.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Weekly Insights Tab ---
with tab_insights:
    st.subheader("Weekly Spending Insights")
    if st.button("Load Insights"):
        try:
            resp = requests.get(f"{backend_url}/insights/weekly", timeout=10)
            insights = resp.json()
            st.write(f"Total spent this week: ${insights['total_spent']:.2f}")
            st.write("By category:")
            for cat, amt in insights['by_category'].items():
                st.write(f"- {cat}: ${amt:.2f}")
            st.write(f"Transaction count: {insights['transaction_count']}")
        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    if st.button("🗑️ Clear Memory"):
        try:
            requests.delete(f"{backend_url}/memory")
            st.success("Memory cleared.")
        except Exception as e:
            st.error(f"Error: {e}")
    if st.button("Generate Insight"):
        try:
            resp = requests.get(f"{backend_url}/insights/weekly", timeout=30)
            data = resp.json()
            st.markdown(f"**Period:** {data['period']}")
            st.markdown(f"**Total Spent:** ${data['total_spent']:,.2f}")
            st.write(data["summary"])
            if data["top_categories"]:
                st.subheader("Top Categories")
                st.dataframe(pd.DataFrame(data["top_categories"]))
        except Exception as e:
            st.error(f"Error: {e}")
