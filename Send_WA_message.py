# PYTHON_TASKS_LW/whatsapp_scheduled.py

import streamlit as st
import pywhatkit as kit
import datetime

def run():
    st.subheader("📅 Schedule WhatsApp Message via PyWhatKit")

    number = st.text_input("📱 Receiver's WhatsApp Number (with country code)", "+91")
    message = st.text_area("💬 Message", "Your gf is just doing her work so ignore this message 😄")

    # Set default to 1 min later to give time for browser to load
    now = datetime.datetime.now()
    default_hour = now.hour
    default_minute = (now.minute + 1) % 60

    col1, col2 = st.columns(2)
    with col1:
        hour = st.number_input("Hour (24-hour format)", min_value=0, max_value=23, value=default_hour)
    with col2:
        minute = st.number_input("Minute", min_value=0, max_value=59, value=default_minute)

    if st.button("🚀 Schedule Message"):
        try:
            st.info("⌛ Opening WhatsApp Web... Don't close the terminal or browser.")
            kit.sendwhatmsg(number, message, int(hour), int(minute), wait_time=15)
            st.success("✅ Message scheduled! It will be sent via WhatsApp Web.")
        except Exception as e:
            st.error(f"❌ Failed to schedule message: {e}")
