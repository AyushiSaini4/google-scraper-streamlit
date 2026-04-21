# PYTHON_TASKS_LW/linkedin_poster.py

import streamlit as st
import requests
import json

def run():
    st.subheader("💼 Post to LinkedIn via API")

    access_token = st.text_input("🔑 LinkedIn Access Token", type="password")
    post_text = st.text_area("📝 Post Content", "Hello LinkedIn! This post was made using Python 🚀")

    if st.button("📤 Publish to LinkedIn"):
        if not access_token or not post_text.strip():
            st.warning("Please provide both access token and content.")
            return

        try:
            # Get LinkedIn user ID
            profile_url = "https://api.linkedin.com/v2/me"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            profile_response = requests.get(profile_url, headers=headers)

            if profile_response.status_code != 200:
                st.error(f"❌ Failed to fetch LinkedIn profile: {profile_response.text}")
                return

            profile_data = profile_response.json()
            linkedin_id = profile_data.get("id")

            # Prepare post payload
            post_url = "https://api.linkedin.com/v2/ugcPosts"
            post_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            post_data = {
                "author": f"urn:li:person:{linkedin_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": post_text},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            response = requests.post(post_url, headers=post_headers, data=json.dumps(post_data))

            if response.status_code == 201:
                st.success("✅ LinkedIn post published successfully!")
            else:
                st.error(f"❌ Failed to post: {response.status_code} {response.text}")

        except Exception as e:
            st.error(f"Unexpected error: {e}")
