import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Flashcards", page_icon="♡", layout="centered")

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
        df = pd.read_csv("flashcards.csv")
        df.columns = df.columns.str.strip()  # Remove extra spaces from column names
        if "Korean" not in df.columns or "English" not in df.columns:
            st.error("⚠️ CSV must have 'Korean' and 'English' columns.")
            return []

        # Clean up values: remove quotes, trailing commas and whitespace
        df["English"] = df["English"].astype(str).str.strip('", ').str.strip()
        df["Korean"] = df["Korean"].astype(str).str.strip()

        return df.to_dict(orient="records")
    except FileNotFoundError:
        st.error("⚠️ flashcards.csv not found! Please make sure it's in the same folder.")
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
    st.session_state.correct = 0
    st.session_state.total = 0
    st.session_state.direction = "Korean to English"

st.sidebar.title("Options")
direction = st.sidebar.radio("Flashcard Direction", ["Korean to English", "English to Korean"])
st.session_state.direction = direction

search_term = st.sidebar.text_input("Search a word")
if search_term:
    filtered_cards = [
        card for card in flashcards
        if search_term.lower() in card["Korean"].lower() or search_term.lower() in card["English"].lower()
    ]
    if filtered_cards:
        flashcards = filtered_cards
        st.session_state.index = 0
    else:
        st.warning("No matches found.")

card = flashcards[st.session_state.index]

st.title("Flashcards")
if st.session_state.direction == "Korean to English":
    st.markdown(f"<h2>{card['Korean']}</h2>", unsafe_allow_html=True)
    answer = card['English']
else:
    st.markdown(f"<h2>{card['English']}</h2>", unsafe_allow_html=True)
    answer = card['Korean']

if st.button("Show Answer 💡"):
    st.session_state.show_answer = True

if st.session_state.get("show_answer", False):
    st.markdown(f"<h3>{answer}</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ I got it right"):
            st.session_state.correct += 1
            st.session_state.total += 1
            st.session_state.index = (st.session_state.index + 1) % len(flashcards)
            st.session_state.show_answer = False
            st.rerun()
    with col2:
        if st.button("❌ I got it wrong"):
            st.session_state.total += 1
            st.session_state.index = (st.session_state.index + 1) % len(flashcards)
            st.session_state.show_answer = False
            st.rerun()

if st.session_state.total > 0:
    score = st.session_state.correct / st.session_state.total * 100
    st.sidebar.metric("Accuracy", f"{score:.1f}%")
    st.sidebar.write(f"{st.session_state.correct} out of {st.session_state.total} correct")

