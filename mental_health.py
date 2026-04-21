# PYTHON_TASKS_LW/mental_health_checkin.py

import streamlit as st
from datetime import datetime
import random
import csv

questions = [
    "1. How happy do you feel today?",
    "2. How energetic are you?",
    "3. How well did you sleep?",
    "4. How anxious or stressed do you feel?",
    "5. How motivated are you today?"
]

selfcare_tips = {
    "Happy": [
        "Keep up the good energy! Maybe share your joy with a friend today 💬",
        "Do something creative — paint, write, dance, or sing 🎨"
    ],
    "Balanced": [
        "Try journaling or planning tomorrow 📝",
        "Take a 15-minute mindful walk 🌳"
    ],
    "Low": [
        "Drink water and take a power nap 💤",
        "Listen to calming music or call someone you trust 🎧"
    ],
    "Down": [
        "Try deep breathing for 5 minutes. You're doing your best 💖",
        "Write down 3 things you’re grateful for 🙏"
    ]
}

quotes = [
    "“You don't have to control your thoughts. You just have to stop letting them control you.” – Dan Millman",
    "“This too shall pass.”",
    "“You are stronger than you think.”",
    "“One small positive thought in the morning can change your whole day.”",
    "“Healing takes time, and that’s okay.”"
]

def analyze_mood(scores):
    mood_score = sum(scores)
    avg = mood_score / len(scores)

    if avg >= 4.5:
        mood = "😄 Happy & Thriving"
    elif avg >= 3.5:
        mood = "🙂 Balanced & Calm"
    elif avg >= 2.5:
        mood = "😕 Low & Tired"
    else:
        mood = "😞 Down & Anxious"

    return mood, mood_score

def get_selfcare_tip(mood):
    if "Happy" in mood:
        return random.choice(selfcare_tips["Happy"])
    elif "Balanced" in mood:
        return random.choice(selfcare_tips["Balanced"])
    elif "Low" in mood:
        return random.choice(selfcare_tips["Low"])
    else:
        return random.choice(selfcare_tips["Down"])

def save_log(name, mood_score):
    with open("mental_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime('%Y-%m-%d'), name, mood_score])

def run():
    st.title("💖 Mental Health Check-in")

    name = st.text_input("What's your name?", "")

    if name:
        st.markdown("Please rate the following on a scale from 1 (lowest) to 5 (highest):")
        scores = []

        for q in questions:
            score = st.slider(q, min_value=1, max_value=5, value=3)
            scores.append(score)

        if st.button("🧠 Analyze My Mood"):
            mood, mood_score = analyze_mood(scores)

            st.markdown(f"### 📊 {name}, your mood score is **{mood_score}/25**")
            st.markdown(f"### 🌈 Mood Status: **{mood}**")

            st.markdown("### 🧘 Self-care Tip of the Day")
            st.info(get_selfcare_tip(mood))

            st.markdown("### 💡 Motivational Quote")
            st.success(random.choice(quotes))

            save_log(name, mood_score)
            st.success("✅ Your mood log has been saved to `mental_log.csv`. Take care! 💗")
