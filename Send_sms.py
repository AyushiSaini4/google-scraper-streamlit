# PYTHON_TASKS_LW/sms_sender.py

import streamlit as st
from twilio.rest import Client

def run():
    st.subheader("📤 Send SMS via Twilio")

    st.markdown("🔐 Make sure to use a verified number when using Twilio trial.")

    # Twilio credentials input
    account_sid = st.text_input("Twilio Account SID", type="password")
    auth_token = st.text_input("Twilio Auth Token", type="password")
    twilio_number = st.text_input("Twilio Phone Number", "+15208415744")
    recipient_number = st.text_input("Recipient Number (with country code)", "+91")
    message_body = st.text_area("Message", "Hello! This is a test message sent using Python 😄")

    if st.button("Send SMS"):
        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=recipient_number
            )
            st.success(f"✅ Message sent successfully! SID: {message.sid}")
        except Exception as e:
            st.error(f"❌ Failed to send SMS. Error: {e}")

