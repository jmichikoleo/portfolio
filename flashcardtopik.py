import streamlit as st
import random
import pandas as pd


st.set_page_config(page_title="Flashcards")
st.markdown("""
    <style>
        .main {background-color: #ffc0cb;}
        h1, h2, h3, p {color: #fff !important; text-align: center;}
        .stButton button {background-color: #ff69b4 !important; color: white !important; border-radius: 10px; font-size: 20px;}
    </style>
""", unsafe_allow_html=True)

def load_flashcards():
    try:
        df = pd.read_csv("flashcards.csv")  
        return df.to_dict(orient="records") 
    except FileNotFoundError:
        st.error("⚠️ flashcards.csv not found! Please add the file to the project folder.")
        return []

flashcards = load_flashcards()
if not flashcards:
    st.stop()  

random.shuffle(flashcards)

if "index" not in st.session_state:
    st.session_state.index = 0

card = flashcards[st.session_state.index]

st.title("Flashcards")

st.markdown(f"<h2>{card['Korean']}</h2>", unsafe_allow_html=True)

if st.button("Show Answer 💡"):
    st.markdown(f"<h3>{card['English']}</h3>", unsafe_allow_html=True)

if st.button("Next ➡️"):
    st.session_state.index = (st.session_state.index + 1) % len(flashcards)
    st.rerun()
