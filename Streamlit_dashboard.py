import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import csv
import json
from datetime import datetime
import random
import os
import smtplib
from email.message import EmailMessage
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- Section 1: Mental Health Check-in ----------
def mental_health_section():
    st.header("💌 Mental Health Check-in")
    name = st.text_input("Your name")

    questions = [
        "How happy do you feel today?",
        "How energetic are you?",
        "How well did you sleep?",
        "How anxious or stressed do you feel?",
        "How motivated are you today?"
    ]

    scores = [st.slider(q, 1, 5, 3) for q in questions]

    if st.button("Submit Mood Check"):
        mood_score = sum(scores)
        avg = mood_score / len(scores)

        mood = ("😄 Happy & Thriving" if avg >= 4.5 else
                "🙂 Balanced & Calm" if avg >= 3.5 else
                "😕 Low & Tired" if avg >= 2.5 else
                "😞 Down & Anxious")

        st.success(f"Mood Score: {mood_score}/25 | Status: {mood}")

        tips = {
            "Happy": ["Share your joy 💬", "Do something creative 🎨"],
            "Balanced": ["Try journaling 📝", "Take a mindful walk 🌳"],
            "Low": ["Hydrate and rest 💤", "Listen to music or call someone 🎧"],
            "Down": ["Deep breathing 💖", "Write 3 things you’re grateful for 🙏"]
        }

        for key in tips:
            if key in mood:
                st.info(f"🧘 Tip: {random.choice(tips[key])}")

        quote = random.choice([
            "You are stronger than you think.",
            "Healing takes time, and that’s okay.",
            "This too shall pass."
        ])
        st.caption(f"💡 Motivation: {quote}")

        with open('mental_log.csv', 'a', newline='') as f:
            csv.writer(f).writerow([datetime.now().strftime('%Y-%m-%d'), name, mood_score])


# ---------- Section 2: Habit Tracker ----------
def habit_tracker_section():
    st.header("📈 Habit Tracker")
    DATA_FILE = "habit_data.json"

    def load_data():
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {"habits": [], "progress": {}, "xp": 0}

    def save_data(data):
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def get_streak(dates_list):
        if not dates_list:
            return 0
        dates = sorted([datetime.strptime(d, '%Y-%m-%d') for d in dates_list])
        streak = 1
        for i in range(len(dates) - 1, 0, -1):
            if (dates[i] - dates[i - 1]).days == 1:
                streak += 1
            else:
                break
        return streak

    data = load_data()
    new_habit = st.text_input("Add a new habit")
    if st.button("Add Habit") and new_habit:
        if new_habit not in data['habits']:
            data['habits'].append(new_habit)
            data['progress'][new_habit] = []
            save_data(data)
            st.success(f"Added habit: {new_habit}")
        else:
            st.warning("Habit already exists.")

    if data['habits']:
        selected_habit = st.selectbox("Mark a habit as done today", data['habits'])
        if st.button("Mark as Done"):
            today = datetime.today().strftime('%Y-%m-%d')
            if today not in data['progress'][selected_habit]:
                data['progress'][selected_habit].append(today)
                data['xp'] += 10
                st.success(f"✅ +10 XP for '{selected_habit}'")
                save_data(data)
            else:
                st.info("Already marked for today.")

        st.subheader("🎯 Progress Overview")
        for habit in data['habits']:
            streak = get_streak(data['progress'][habit])
            st.write(f"- {habit}: {len(data['progress'][habit])} days ✅, Streak: {streak} 🔥")

        st.write(f"🏆 Total XP: {data['xp']}")


# ---------- Section 3: Carbon Footprint Tracker ----------
def carbon_footprint_section():
    st.header("🌍 Carbon Footprint Calculator")
    name = st.text_input("Enter your name")
    car_km = st.number_input("Daily car travel (km)", 0.0)
    bus_km = st.number_input("Daily bus travel (km)", 0.0)
    bike_km = st.number_input("Daily bike travel (km)", 0.0)
    electricity = st.number_input("Monthly electricity usage (kWh)", 0.0)
    water = st.number_input("Daily water usage (litres)", 0.0)
    diet = st.selectbox("Diet Type", ['vegan', 'vegetarian', 'non-veg'])
    shopping = st.selectbox("Shopping Frequency", ['low', 'medium', 'high'])

    if st.button("Calculate Footprint"):
        score = (
            (car_km * 0.21 + bus_km * 0.1 + bike_km * 0.02) * 30 +
            electricity * 0.92 + water * 30 * 0.0015 +
            {'vegan': 2.0, 'vegetarian': 2.5, 'non-veg': 3.3}[diet] * 30 +
            {'low': 5, 'medium': 15, 'high': 30}[shopping]
        )
        score = round(score, 2)
        st.success(f"Monthly carbon footprint: {score} kg CO₂")
        with open('carbon_log.csv', 'a', newline='') as f:
            csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), name, score])


# ---------- Section 4: Digital Art Generator ----------
def digital_art_section():
    st.header("🎨 Create Your Digital Art")
    if st.button("Generate Art"):
        img = Image.new('RGB', (400, 400), color='lightblue')
        draw = ImageDraw.Draw(img)
        draw.rectangle([(50, 50), (350, 350)], outline='blue', width=5)
        draw.ellipse([(150, 150), (250, 250)], fill='yellow', outline='black')
        draw.text((120, 180), "Hi Ayushi!", fill="black")
        img.save("my_digital_art.png")
        st.image("my_digital_art.png")
        st.success("✅ Art saved as my_digital_art.png")


# ---------- Section 5: Anonymous Email Sender ----------
def anonymous_email_section():
    st.header("📧 Send Anonymous Email")
    recipient = st.text_input("Recipient Email")
    message = st.text_area("Message")
    if st.button("Send Email"):
        sender_email = "sainiayushi2004@gmail.com"
        app_password = "kmow vxbw wsya ykpb"
        msg = EmailMessage()
        msg['Subject'] = 'Anonymous Feedback'
        msg['From'] = 'Anonymous Sender sainiayushi2004@gmail.com'
        msg['To'] = recipient
        msg.set_content(message)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, app_password)
                smtp.send_message(msg)
            st.success("✅ Email sent anonymously!")
        except Exception as e:
            st.error(f"Failed to send email: {e}")


# ---------- Section 6: LLaMA vs DeepSeek Comparison ----------
def ai_model_compare_section():
    st.header("🧠 LLaMA vs DeepSeek AI")

    llama_tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    llama_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", torch_dtype=torch.float16, device_map="auto")

    deepseek_tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-llm-7b-chat")
    deepseek_model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-llm-7b-chat", torch_dtype=torch.float16, device_map="auto")

    topic = st.text_input("Ask a topic or question")
    if st.button("Compare Models") and topic:
        def generate_response(model, tokenizer, prompt):
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(**inputs, max_new_tokens=300, temperature=0.7)
            return tokenizer.decode(outputs[0], skip_special_tokens=True)

        llama_response = generate_response(llama_model, llama_tokenizer, topic)
        deepseek_response = generate_response(deepseek_model, deepseek_tokenizer, topic)

        st.subheader("🦙 LLaMA Response")
        st.text(llama_response)
        st.subheader("🐉 DeepSeek Response")
        st.text(deepseek_response)

        vec = TfidfVectorizer().fit_transform([llama_response, deepseek_response])
        sim_score = cosine_similarity(vec[0:1], vec[1:2])[0][0]
        st.write(f"🔍 Similarity Score: {sim_score:.2f}")


# ---------- Streamlit App ----------
st.set_page_config(page_title="Ayushi's Dashboard", layout="centered")
st.title("✨ Ayushi's All-in-One Streamlit Dashboard")

option = st.sidebar.selectbox("Choose a Module", [
    "Mental Health Check-in",
    "Habit Tracker",
    "Carbon Footprint Calculator",
    "Digital Art Generator",
    "Anonymous Email Sender",
    "AI Model Comparison"
])

if option == "Mental Health Check-in":
    mental_health_section()
elif option == "Habit Tracker":
    habit_tracker_section()
elif option == "Carbon Footprint Calculator":
    carbon_footprint_section()
elif option == "Digital Art Generator":
    digital_art_section()
elif option == "Anonymous Email Sender":
    anonymous_email_section()
elif option == "AI Model Comparison":
    ai_model_compare_section()
