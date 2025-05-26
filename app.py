import os
import re
import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Instantiate the HF Inference client
client = InferenceClient(
    provider="auto",
    api_key=os.environ["HUGGINGFACEHUB_API_TOKEN"]
)

st.set_page_config(page_title="Educational Chatbot", layout="wide")
st.title("🎓 Educational Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []  # list of (sender, message)

def build_messages():
    return [
        {"role": "user" if s == "You" else "assistant", "content": m}
        for s, m in st.session_state.history
    ]

def clean_think_tags(text: str) -> str:
    # remove <think>...</think> blocks
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# Render chat history
for sender, msg in st.session_state.history:
    if sender == "You":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)

# Input
user_input = st.chat_input("Ask me anything…")

if user_input:
    # show user turn
    st.session_state.history.append(("You", user_input))
    st.chat_message("user").write(user_input)

    # placeholder for assistant
    placeholder = st.chat_message("assistant")
    placeholder.write("⏳ Thinking...")

    # call HF chat endpoint with entire history
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=build_messages()
        )
        raw = response.choices[0].message["content"]
        # clean out think tags
        reply = clean_think_tags(raw)
    except Exception as e:
        reply = f"❌ API Error: {e}"

    # display and store cleaned reply
    placeholder.write(reply)
    st.session_state.history.append(("Bot", reply))
