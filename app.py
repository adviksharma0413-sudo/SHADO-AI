
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
    "GPT OSS 120B": "openai/gpt-oss-120b",
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

COHERE_MODELS = {
    "Command A": "command-a-03-2025",
}

CLOUDFLARE_MODELS = {
    "Llama 3.1 8B FP8": "@cf/meta/llama-3.1-8b-instruct-fp8",
}


# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:

    st.header("⚙️ SHΛDØ Settings")

    provider = st.selectbox(
        "Choose AI Provider",
        [
            "Groq",
            "OpenRouter",
            "Cohere",
            "Cloudflare Workers AI"
        ]
    )

    if provider == "Groq":
        selected_model = st.selectbox(
            "Choose Model",
            list(GROQ_MODELS.keys())
        )
        model = GROQ_MODELS[selected_model]

    elif provider == "OpenRouter":
        selected_model = st.selectbox(
            "Choose Model",
            list(OPENROUTER_MODELS.keys())
        )
        model = OPENROUTER_MODELS[selected_model]

    elif provider == "Cohere":
        selected_model = st.selectbox(
            "Choose Model",
            list(COHERE_MODELS.keys())
        )
        model = COHERE_MODELS[selected_model]

    else:
        selected_model = st.selectbox(
            "Choose Model",
            list(CLOUDFLARE_MODELS.keys())
        )
        model = CLOUDFLARE_MODELS[selected_model]

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("SHΛDØ AI | Four AI Providers")


# --------------------------------
# API CLIENT
# --------------------------------

if provider == "Groq":

    api_key = read_secret("GROQ_API_KEY")
    base_url = "https://api.groq.com/openai/v1"

elif provider == "OpenRouter":

    api_key = read_secret("OPENROUTER_API_KEY")
    base_url = "https://openrouter.ai/api/v1"

elif provider == "Cohere":

    api_key = read_secret("COHERE_API_KEY")
    base_url = "https://api.cohere.ai/compatibility/v1"

else:

    api_key = read_secret("CLOUDFLARE_API_TOKEN")
    account_id = read_secret("CLOUDFLARE_ACCOUNT_ID")

    if not account_id:
        st.error(
            "Cloudflare Account ID missing. "
            "Check Streamlit Secrets."
        )
        st.stop()

    base_url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/v1"
    )


if not api_key:
    st.error(
        f"{provider} API key missing. "
        "Check your Streamlit Secrets."
    )
    st.stop()


client = OpenAI(
    api_key=api_key,
    base_url=base_url,
    timeout=90.0
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
            with st.spinner("🌑 SHΛDØ is thinking..."):

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are SHΛDØ AI, a helpful, "
                                "intelligent AI assistant."
                            )
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
