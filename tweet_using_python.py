# PYTHON_TASKS_LW/tweet_post.py

import streamlit as st
import tweepy

def run():
    st.subheader("🐦 Post a Tweet using Tweepy")

    # Input tweet text
    tweet_text = st.text_area("Enter your tweet", "Hello, world! 🌍 #Python")

    # Input API credentials
    st.markdown("### 🔐 Twitter API Credentials (keep them secret)")
    api_key = st.text_input("API Key")
    api_secret = st.text_input("API Secret", type="password")
    access_token = st.text_input("Access Token")
    access_token_secret = st.text_input("Access Token Secret", type="password")

    if st.button("Post Tweet"):
        if tweet_text.strip() == "":
            st.warning("Tweet cannot be empty!")
            return

        try:
            # Authenticate
            auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
            api = tweepy.API(auth)

            # Post the tweet
            api.update_status(tweet_text)
            st.success("✅ Tweet posted successfully!")

        except Exception as e:
            st.error(f"❌ Failed to post tweet. Error: {e}")
try:
    # your tweepy logic
    print("✅ Code ran successfully")
except Exception as e:
    print(f"❌ Error: {e}")
