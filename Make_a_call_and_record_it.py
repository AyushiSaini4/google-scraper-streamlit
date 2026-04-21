# PYTHON_TASKS_LW/twilio_voice_call.py

import streamlit as st
from twilio.rest import Client

def run():
    st.subheader("📞 Make a Voice Call via Twilio")

    # Input fields
    account_sid = st.text_input("Twilio Account SID", type="password")
    auth_token = st.text_input("Twilio Auth Token", type="password")
    from_number = st.text_input("Twilio Number (from)", "+xxxxxxxxxxx")
    to_number = st.text_input("Recipient Number (to)", "+91xxxxxxxxxx")
    voice_url = st.text_input(
        "Voice XML URL",
        "http://demo.twilio.com/docs/voice.xml",
        help="Public URL with TwiML instructions (XML)"
    )

    if st.button("📞 Initiate Call"):
        try:
            client = Client(account_sid, auth_token)
            call = client.calls.create(
                to=to_number,
                from_=from_number,
                url=voice_url
            )
            st.success(f"✅ Call initiated! Call SID: {call.sid}")
        except Exception as e:
            st.error(f"❌ Error initiating call: {e}")
