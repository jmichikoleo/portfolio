import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Flashcards", page_icon="🃏", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #ffe4e1;
        }
        .stApp {
            background-color: #ffe4e1;
        }
        h1, h2, h3 {
            color: #4b0082 !important;
            text-align: center;
        }
        .stButton>button {
            background-color: #ff69b4;
            color: white;
            border-radius: 12px;
            font-size: 18px;
            margin: auto;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_flashcards():
    try:
        df = pd.read_excel("flashcards.xls", engine="xlrd")  
        if "Korean" not in df.columns or "English" not in df.columns:
            st.error("⚠️ Excel must have 'Korean' and 'English' columns.")
            return []
        return df.to_dict(orient="records")
    except FileNotFoundError:
        st.error("⚠️ flashcards.xlsx not found! Add it to your project folder.")
        return []
    except Exception as e:
        st.error(f"⚠️ Error loading flashcards: {e}")
        return []

flashcards = load_flashcards()
if not flashcards:
    st.stop()

if "index" not in st.session_state:
    random.shuffle(flashcards)
    st.session_state.index = 0
    st.session_state.show_answer = False

card = flashcards[st.session_state.index]

st.title("Flashcards")
st.markdown(f"<h2>{card['Korean']}</h2>", unsafe_allow_html=True)

if st.button("Show Answer 💡"):
    st.session_state.show_answer = True

if st.session_state.get("show_answer", False):
    st.markdown(f"<h3>{card['English']}</h3>", unsafe_allow_html=True)

if st.button("Next ➡️"):
    st.session_state.index = (st.session_state.index + 1) % len(flashcards)
    st.session_state.show_answer = False
    st.rerun()
