# PYTHON_TASKS_LW/download_webpage.py

import streamlit as st
import requests

def run():
    st.subheader("🌐 Download Web Page")

    url = st.text_input("Enter the URL of the webpage", "https://console.twilio.com")

    if st.button("Download Page"):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text

                # Show preview
                st.success("✅ Webpage downloaded successfully!")
                st.text_area("HTML Preview", html_content[:1000], height=300)  # Show first 1000 chars

                # Let user download the file
                st.download_button(
                    label="📥 Download HTML file",
                    data=html_content,
                    file_name="downloaded_page.html",
                    mime="text/html"
                )

            else:
                st.error(f"❌ Failed to download page. Status code: {response.status_code}")

        except Exception as e:
            st.error(f"Error occurred: {e}")
try:
    # Your existing code
    print("✅ HTML content downloaded")
except Exception as e:
    print(f"❌ Error occurred: {e}")
