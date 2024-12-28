import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_option_menu import option_menu

conn = sqlite3.connect("workout_tracker.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    date TEXT,
    exercise TEXT,
    reps INTEGER,
    sets INTEGER,
    weight INTEGER
)
""")
conn.commit()

def save_workout(user_id, date, exercise, reps, sets, weight):
    cursor.execute("""
    INSERT INTO workouts (user_id, date, exercise, reps, sets, weight) 
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, date, exercise, reps, sets, weight))
    conn.commit()

def get_workouts(user_id):
    query = f"SELECT * FROM workouts WHERE user_id = '{user_id}'"
    return pd.read_sql_query(query, conn)

st.session_state.setdefault("authenticated", False)

def authenticate(username, password):
    return username == "michikoleo" and password == "michikoleo"

def login():
    with st.form("Login"):
        st.write("Login to Gym Rep Counter")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if authenticate(username, password):
                st.session_state["authenticated"] = True
                st.session_state["user_id"] = username
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

if not st.session_state.get("authenticated"):
    login()
else:
    # Main App
    st.title("Gym Rep Counter")
    user_id = st.session_state.get("user_id")

    with st.sidebar:
        selected = option_menu(
            "Navigation",
            ["Home", "Progress", "Logout"],
            icons=["house", "bar-chart", "door-closed"],
            menu_icon="list",
            default_index=0,
        )

    if selected == "Home":
        st.subheader("Add Your Workout")
        date = st.date_input("Date", datetime.now().date())
        exercise = st.text_input("Exercise")
        reps = st.number_input("Reps", min_value=1, step=1)
        sets = st.number_input("Sets", min_value=1, step=1)
        weight = st.number_input("Weight (kg)", min_value=0, step=1)

        if st.button("Save Workout"):
            save_workout(user_id, date.strftime("%Y-%m-%d"), exercise, reps, sets, weight)
            st.success("Workout saved!")

    elif selected == "Progress":
        st.subheader("Your Progress")
        df = get_workouts(user_id)

        if df.empty:
            st.info("No workout data found. Start logging your workouts!")
        else:
            st.dataframe(df)

            daily = df[df["date"] == datetime.now().strftime("%Y-%m-%d")]
            st.write("### Today's Progress")
            st.write(daily)

            one_week_ago = datetime.now() - timedelta(days=7)
            weekly = df[pd.to_datetime(df["date"]) >= one_week_ago]

            one_month_ago = datetime.now() - timedelta(days=30)
            monthly = df[pd.to_datetime(df["date"]) >= one_month_ago]

            one_year_ago = datetime.now() - timedelta(days=365)
            yearly = df[pd.to_datetime(df["date"]) >= one_year_ago]

            st.write("### Progress Graphs")

            def create_graph(data, title):
                if data.empty:
                    st.write(f"No data for {title.lower()}.")
                else:
                    fig = px.line(
                        data,
                        x="date",
                        y="reps",
                        color="exercise",
                        title=title,
                        labels={"reps": "Reps", "date": "Date"},
                    )
                    st.plotly_chart(fig)


            create_graph(weekly, "Weekly Progress")
            create_graph(monthly, "Monthly Progress")
            create_graph(yearly, "Yearly Progress")

    elif selected == "Logout":
        st.session_state["authenticated"] = False
        st.session_state["user_id"] = None  # Clear the user_id too
        st.success("Logged out successfully!")
        st.experimental_rerun()

