import os 
import streamlit as st
import requests

st.set_page_config(
    page_title="Financial Market Intelligence Assistant",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Financial Market Intelligence Assistant")
st.caption("CrewAI + RAG + FAISS + FastAPI + Gemini")

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/query")

if "messages" not in st.session_state:
    st.session_state.messages = []

risk_appetite = st.sidebar.selectbox(
    "Select Risk Appetite",
    ["low", "medium", "high"],
    index=1
)

st.sidebar.markdown("---")
st.sidebar.info(
    "This assistant provides educational financial intelligence only. "
    "It is not financial advice."
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input("Ask a financial market question...")

if user_query:
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Running CrewAI financial agents..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "query": user_query,
                        "risk_appetite": risk_appetite
                    },
                    timeout=180
                )

                if response.status_code == 200:
                    result = response.json()["response"]
                else:
                    result = f"API Error: {response.status_code}\n\n{response.text}"

            except Exception as e:
                result = f"Error connecting to FastAPI backend: {str(e)}"

            st.markdown(result)

    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })
