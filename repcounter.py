import streamlit as st
import pandas as pd
from datetime import date

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "workout_data" not in st.session_state:
    st.session_state.workout_data = pd.DataFrame(columns=["Workout", "Weight", "Reps", "Sets", "Date"])

users = {"michikoleo": "michikoleo", "emily": "emily"}

def login_page():
    """Display login page."""
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials.")

def dashboard():
    """Display the workout dashboard."""
    st.title("Gym Rep Counter Dashboard")

    with st.form("add_workout_form"):
        st.subheader("Add New Workout")
        workout = st.text_input("Workout Name")
        weight = st.text_input("Weight (kg)", value="Bodyweight")
        reps = st.number_input("Reps per Set", min_value=1, value=10)
        sets = st.number_input("Total Sets", min_value=1, value=1)
        submitted = st.form_submit_button("Add Workout")

        if submitted:
            new_workout = {
                "Workout": workout,
                "Weight": weight,
                "Reps": reps,
                "Sets": sets,
                "Date": date.today().strftime("%Y-%m-%d")
            }
            st.session_state.workout_data = st.session_state.workout_data.append(new_workout, ignore_index=True)
            st.success("Workout added successfully!")

    st.subheader("Today's Workouts")
    today_data = st.session_state.workout_data[st.session_state.workout_data["Date"] == date.today().strftime("%Y-%m-%d")]
    st.table(today_data)

    st.subheader("Progress")
    weekly_progress = len(today_data)
    st.metric(label="Workouts Completed Today", value=weekly_progress)

    if st.button("Logout"):
        st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
else:
    dashboard()
