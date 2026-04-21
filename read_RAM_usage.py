# LINUX_TASKS/ram_usage.py (or PYTHON_TASKS_LW/ram_usage.py)

import streamlit as st
import psutil

def run():
    st.subheader("🧠 RAM Usage Monitor")

    memory = psutil.virtual_memory()

    total = memory.total / (1024 ** 3)
    available = memory.available / (1024 ** 3)
    used = memory.used / (1024 ** 3)
    percent = memory.percent

    st.metric(label="💾 Total RAM", value=f"{total:.2f} GB")
    st.metric(label="🟢 Available RAM", value=f"{available:.2f} GB")
    st.metric(label="🔴 Used RAM", value=f"{used:.2f} GB")
    st.metric(label="📊 Usage Percentage", value=f"{percent}%")

    st.progress(percent / 100)
