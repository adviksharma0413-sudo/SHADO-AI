
import os
import streamlit as st
from openai import OpenAI


# --------------------------------
# SHΛDØ AI — CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="SHΛDØ AI",
    page_icon="🌑",
    layout="wide"
)

st.title("🌑 SHΛDØ AI")
st.caption("Your personal multi-model AI assistant")


# --------------------------------
# API KEY LOADER
# --------------------------------

def read_secret(name):
    try:
        value = st.secrets.get(name)
        if value:
            return value
    except Exception:
        pass

    return os.getenv(name)


# --------------------------------
# PROVIDERS AND MODELS
# --------------------------------

GROQ_MODELS = {
    "GPT OSS 120B (Recommended)": "openai/gpt-oss-120b",
    "GPT OSS 20B": "openai/gpt-oss-20b",
    "Llama 4 Scout": "meta-llama/llama-4-scout-17b-16e-instruct",
}

OPENROUTER_MODELS = {
    "Auto": "openrouter/auto",
    "Llama 3.3 70B": "meta-llama/llama-3.3-70b-instruct",
    "DeepSeek R1": "deepseek/deepseek-r1",
    "Qwen3 235B": "qwen/qwen3-235b-a22b",
    "Gemini 2.5 Flash": "google/gemini-2.5-flash",
    "Claude Sonnet 4": "anthropic/claude-sonnet-4",
    "GPT-4.1": "openai/gpt-4.1",
}


# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:
    st.header("⚙️ SHΛDØ Settings")

    provider = st.selectbox(
        "Choose AI Provider",
        ["Groq", "OpenRouter"]
    )

    if provider == "Groq":
        selected_model = st.selectbox(
            "Choose Model",
            list(GROQ_MODELS.keys())
        )
        model = GROQ_MODELS[selected_model]

    else:
        selected_model = st.selectbox(
            "Choose Model",
            list(OPENROUTER_MODELS.keys())
        )
        model = OPENROUTER_MODELS[selected_model]

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("SHΛDØ AI | Multi-model assistant")


# --------------------------------
# API CLIENT
# --------------------------------

if provider == "Groq":
    api_key = read_secret("GROQ_API_KEY")

    if not api_key:
        st.error("Groq API key missing. Add GROQ_API_KEY in Streamlit Secrets.")
        st.stop()

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

else:
    api_key = read_secret("OPENROUTER_API_KEY")

    if not api_key:
        st.error("OpenRouter API key missing. Add OPENROUTER_API_KEY in Streamlit Secrets.")
        st.stop()

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )


# --------------------------------
# CHAT HISTORY
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------
# CHAT INPUT
# --------------------------------

prompt = st.chat_input("Message SHΛDØ AI...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("SHΛDØ is thinking..."):

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are SHΛDØ AI, a helpful, intelligent AI assistant."
                        },
                        *st.session_state.messages
                    ]
                )

                answer = response.choices[0].message.content

                if not answer:
                    answer = "The AI returned an empty response."

                st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as e:
            st.error(f"AI Error: {e}")
