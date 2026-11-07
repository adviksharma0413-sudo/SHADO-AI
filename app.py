
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="SHΛDØ AI",
    page_icon="🌑",
    layout="wide"
)

# API key loader
def read_secret(name):
    try:
        value = st.secrets.get(name)
        if value:
            return value
    except Exception:
        pass
    return os.getenv(name)


# Available models
MODELS = {
    "Groq": {
        "Llama 3.3 70B": "llama-3.3-70b-versatile",
        "Llama 4 Scout": "meta-llama/llama-4-scout-17b-16e-instruct",
        "GPT OSS 120B": "openai/gpt-oss-120b",
        "GPT OSS 20B": "openai/gpt-oss-20b",
    },
    "OpenRouter": {
        "Auto (Best available)": "openrouter/auto",
        "Llama 3.3 70B": "meta-llama/llama-3.3-70b-instruct",
        "DeepSeek R1": "deepseek/deepseek-r1",
        "Qwen3 235B": "qwen/qwen3-235b-a22b",
        "Gemini 2.5 Flash": "google/gemini-2.5-flash",
        "Claude Sonnet 4": "anthropic/claude-sonnet-4",
        "GPT-4.1": "openai/gpt-4.1",
    }
}


# Page design
st.title("🌑 SHΛDØ AI")
st.caption("Your personal multi-model AI assistant")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    provider = st.selectbox(
        "Choose AI Provider",
        ["Groq", "OpenRouter"]
    )

    model_name = st.selectbox(
        "Choose AI Model",
        list(MODELS[provider].keys())
    )

    selected_model = MODELS[provider][model_name]

    st.markdown("---")
    st.write(f"**Provider:** {provider}")
    st.write(f"**Model:** {model_name}")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# API response
def get_response(messages, provider, model):
    if provider == "Groq":
        api_key = read_secret("GROQ_API_KEY")
        base_url = "https://api.groq.com/openai/v1"

    else:
        api_key = read_secret("OPENROUTER_API_KEY")
        base_url = "https://openrouter.ai/api/v1"

    if not api_key:
        return f"API key missing! Please configure {provider} API key."

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content


# User input
if prompt := st.chat_input("Message SHΛDØ AI..."):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"SHΛDØ is thinking with {model_name}..."):
            try:
                answer = get_response(
                    st.session_state.messages,
                    provider,
                    selected_model
                )
            except Exception as e:
                answer = f"Error: {e}"

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
