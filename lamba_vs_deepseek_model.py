# PYTHON_TASKS_LW/llm_comparator.py

import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_resource
def load_model_and_tokenizer(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return tokenizer, model

def generate_response(model, tokenizer, prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=300, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def run():
    st.title("🤖 LLaMA 2 vs DeepSeek LLM - Response Comparator")

    topics = [
        "Explain quantum computing in simple terms.",
        "What are the causes of climate change?",
        "How does the Indian economy function?",
        "Describe the impact of AI on healthcare.",
        "Explain the concept of karma in Hinduism.",
    ]
    prompt = st.selectbox("Choose a topic:", topics)
    prompt = st.text_area("Or write your own prompt:", value=prompt)

    if st.button("🔍 Compare Responses"):
        with st.spinner("Loading LLaMA 2 model..."):
            llama_tokenizer, llama_model = load_model_and_tokenizer("meta-llama/Llama-2-7b-chat-hf")

        with st.spinner("Loading DeepSeek model..."):
            deepseek_tokenizer, deepseek_model = load_model_and_tokenizer("deepseek-ai/deepseek-llm-7b-chat")

        llama_response = generate_response(llama_model, llama_tokenizer, prompt)
        deepseek_response = generate_response(deepseek_model, deepseek_tokenizer, prompt)

        st.subheader("🦙 LLaMA 2 Response")
        st.write(llama_response)

        st.subheader("🐉 DeepSeek Response")
        st.write(deepseek_response)

        # Similarity Score
        vec = TfidfVectorizer().fit_transform([llama_response, deepseek_response])
        sim_score = cosine_similarity(vec[0:1], vec[1:2])[0][0]

        st.metric("🔁 Similarity Score", f"{sim_score:.2f}")
