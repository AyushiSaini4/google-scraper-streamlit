# PYTHON_TASKS_LW/voice_call.py

import streamlit as st
from twilio.rest import Client

def run():
    st.subheader("📞 Make a Voice Call using Twilio")

    to_number = st.text_input("Enter the phone number to call (with country code)", "+91")
    call_message = st.text_area("Message to say in the call", "Hello! This is a Python voice call from Twilio.")

    if st.button("Make Call"):
        try:
            # Twilio credentials
            account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
            auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
            twilio_number = '+15208415744'

            client = Client(account_sid, auth_token)

            # Compose the TwiML message
            twiml = f'<Response><Say>{call_message}</Say></Response>'

            # Make the call
            call = client.calls.create(
                twiml=twiml,
                to=to_number,
                from_=twilio_number
            )

            st.success(f"Call initiated successfully! ✅ Call SID: {call.sid}")

        except Exception as e:
            st.error(f"Error placing call: {e}")
print("✅ Script ran successfully")
