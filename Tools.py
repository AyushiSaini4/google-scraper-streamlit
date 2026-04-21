# PYTHON_TASKS_LW/langchain_agent.py
# OLD (deprecated): YOUR_OPENAI_API_KEY
# from langchain_community.llms import OpenAI

# ✅ NEW
from langchain_openai import OpenAI
 
import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_openai import OpenAI

from langchain_community.tools import DuckDuckGoSearchRun
import os
from dotenv import load_dotenv

# Load OpenAI API key from .env
load_dotenv()

def calculator(query: str) -> str:
    try:
        result = eval(query)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def read_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Define all tools
tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Perform Python-style math: 12*5, (100+34)/2"
    ),
    Tool(
        name="WebSearch",
        func=DuckDuckGoSearchRun().run,
        description="Search the web using DuckDuckGo"
    ),
    Tool(
        name="ReadFile",
        func=read_file,
        description="Read the contents of a text file. Input should be full file path."
    )
]

# Initialize LangChain Agent
llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

def run():
    st.subheader("🤖 LangChain Tool Agent")

    query = st.text_area("Ask something (e.g. math, news, file content)", "What is 24 * 7?")

    if st.button("Run Agent"):
        with st.spinner("Processing with LangChain..."):
            try:
                result = agent.run(query)
                st.success("✅ Agent Response:")
                st.markdown(f"> {result}")
            except Exception as e:
                st.error(f"Error: {e}")
