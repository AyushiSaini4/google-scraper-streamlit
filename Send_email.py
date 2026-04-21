# PYTHON_TASKS_LW/email_sender.py

import streamlit as st
import smtplib
from email.mime.text import MIMEText

def run():
    st.subheader("📧 Send Email using Gmail SMTP")

    st.markdown("**Note:** You'll need to [generate a Gmail App Password](https://myaccount.google.com/apppasswords) (not your usual password).")

    # Input fields
    sender = st.text_input("Sender Email", "youremail@gmail.com")
    recipient = st.text_input("Recipient Email", "someone@example.com")
    subject = st.text_input("Subject", "Python Email Test")
    message = st.text_area("Message", "This is a test email from Python using Gmail SMTP.")
    app_password = st.text_input("Gmail App Password", type="password")

    if st.button("📨 Send Email"):
        try:
            # Compose the email
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = recipient

            # Connect and send
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender, app_password)
                server.send_message(msg)

            st.success("✅ Email sent successfully!")

        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
