# PYTHON_TASKS_LW/send_sms.py

import streamlit as st
from twilio.rest import Client

def run():
    st.subheader("📲 Send SMS using Twilio")

    # Get input from user
    to_number = st.text_input("Enter receiver's phone number (with country code)", "+91")
    message_body = st.text_area("Enter your message", "Hello! This is a message sent using Python 📲")

    if st.button("Send SMS"):
        try:
            # Twilio credentials
            account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
            auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
            twilio_number = '+15208415744'

            # Send message
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=to_number
            )
            st.success(f"Message sent successfully! ✅ SID: {message.sid}")
        except Exception as e:
            st.error(f"Failed to send message. Error: {e}")
