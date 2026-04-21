# PYTHON_TASKS_LW/habit_tracker_v2.py

import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "habit_data.json"

# -----------------------------
# Utility Functions
# -----------------------------
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
        delta = (dates[i] - dates[i - 1]).days
        if delta == 1:
            streak += 1
        else:
            break
    return streak


def level_up_message(xp):
    if xp < 50:
        return "🌱 You're just starting out. Keep going!"
    elif xp < 100:
        return "🌿 You're growing strong! Stay consistent."
    elif xp < 200:
        return "🌳 You're crushing it! Almost a Habit Master!"
    else:
        return "👑 HabiKing Mode Activated! You're unstoppable!"


def get_next_level(xp):
    if xp < 50:
        return 50
    elif xp < 100:
        return 100
    elif xp < 200:
        return 200
    else:
        return xp + 100  # every 100 XP after 200 is a new level


# -----------------------------
# Main App
# -----------------------------
def run():
    st.title("📈 Habit Tracker 2.0 — XP, Streaks & Motivation")

    data = load_data()
    today = datetime.today().strftime('%Y-%m-%d')

    # -----------------------------
    # Add New Habit
    # -----------------------------
    st.subheader("➕ Add a New Habit")
    new_habit = st.text_input("Habit name", placeholder="e.g., Read 10 pages")

    if st.button("Add Habit"):
        new_habit = new_habit.strip()
        if new_habit and new_habit.lower() not in [h.lower() for h in data["habits"]]:
            data["habits"].append(new_habit)
            data["progress"][new_habit] = []
            save_data(data)
            st.session_state.habit_added = True
            st.success(f"✅ Habit '{new_habit}' added successfully!")
        else:
            st.warning("⚠️ Habit is empty or already exists.")

    # -----------------------------
    # Mark Habit as Done
    # -----------------------------
    st.subheader("✅ Mark Habit as Done Today")

    if data["habits"]:
        habit_to_mark = st.selectbox("Select a habit", data["habits"])
        if st.button("Mark as Done"):
            if today in data["progress"][habit_to_mark]:
                st.info("👍 You've already marked this habit for today!")
            else:
                data["progress"][habit_to_mark].append(today)
                streak = get_streak(data["progress"][habit_to_mark])
                bonus = 5 if streak >= 7 else 0  # streak reward
                data["xp"] += 10 + bonus
                save_data(data)
                st.success(f"🎯 +{10 + bonus} XP for completing '{habit_to_mark}' today!")
                st.info(level_up_message(data["xp"]))
    else:
        st.warning("No habits added yet. Please add one above.")

    # -----------------------------
    # Manage Habits
    # -----------------------------
    with st.expander("⚙️ Manage Habits"):
        if data["habits"]:
            habit_to_delete = st.selectbox("Select habit to delete", data["habits"])
            if st.button("Delete Habit"):
                data["habits"].remove(habit_to_delete)
                del data["progress"][habit_to_delete]
                save_data(data)
                st.warning(f"🗑️ Habit '{habit_to_delete}' deleted!")
        else:
            st.info("No habits to manage yet.")

    # -----------------------------
    # Progress Overview
    # -----------------------------
    st.subheader("📊 Progress Overview")

    if data["habits"]:
        for habit in data["habits"]:
            done_days = len(data["progress"][habit])
            streak = get_streak(data["progress"][habit])

            st.markdown(f"**{habit}** — {done_days} days ✅, Streak: {streak} 🔥")

            # Calculate habit progress ratio
            if data["progress"][habit]:
                first_day = datetime.strptime(data["progress"][habit][0], "%Y-%m-%d")
                total_days = (datetime.today() - first_day).days + 1
                progress_ratio = done_days / max(1, total_days)
                st.progress(progress_ratio)
    else:
        st.info("Add some habits to start tracking your journey!")

    # -----------------------------
    # XP Overview
    # -----------------------------
    st.subheader("🏆 XP Progress")
    st.metric("Total XP", data["xp"])

    next_level = get_next_level(data["xp"])
    progress_to_next = min(data["xp"] / next_level, 1.0)
    st.progress(progress_to_next, text=f"{data['xp']} / {next_level} XP")

    st.info(level_up_message(data["xp"]))


if __name__ == "__main__":
    run()
