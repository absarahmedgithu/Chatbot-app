import streamlit as st
import requests
import os

# --- Configuration ---
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖", layout="centered")

# --- Load API key ---
GROQ_API_KEY = os.getenv("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")

if not GROQ_API_KEY:
    st.warning("⚠️ Please set your GROQ_API_KEY as an environment variable before running the app.")
    st.stop()

# --- Groq API Endpoint ---
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- Chatbot Function ---
def get_groq_response(messages, model="llama3-8b-8192"):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500,
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# --- Streamlit UI ---
st.title("🤖 Simple Chatbot (Groq API)")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hi! I'm your Groq-powered chatbot. How can I help you today?"}
    ]

# Display chat messages
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**🧑 You:** {chat['content']}")
    else:
        st.markdown(f"**🤖 Bot:** {chat['content']}")

# User input
user_input = st.text_input("Type your message:", placeholder="Ask me anything...")

# Send message
if st.button("Send") and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    response = get_groq_response(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.experimental_rerun()
