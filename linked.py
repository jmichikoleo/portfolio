import streamlit as st
import sqlite3

st.set_page_config(
    page_title="SOTA - Study Smarter",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        body {
            background-color: #f8f9fa;
            font-family: 'Arial', sans-serif;
        }
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
            color: #1a202c;
        }
        .sub-header {
            font-size: 1.2rem;
            text-align: center;
            margin: 10px 0 30px 0;
            color: #4a5568;
        }
        .feature-box {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            background: #fff;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .footer {
            margin-top: 50px;
            font-size: 0.9rem;
            text-align: center;
            color: #718096;
        }
        .footer a {
            color: #2b6cb0;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        .button-container {
            text-align: center;
            margin-top: 30px;
        }
        .link-button {
            background-color: #3182ce;
            color: #FFFFFF;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            font-size: 1rem;
        }
        .link-button:hover {
            background-color: #FFFFFF;
        }
        /* New interactive styles */
        .divider {
            border-bottom: 2px solid #e2e8f0;
            margin: 30px 0;
        }
        .collapsible-container {
            padding: 20px;
            background-color: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
        }
        .collapsible-header {
            font-size: 1.2rem;
            font-weight: bold;
            color: #3182ce;
        }
        .collapsible-content {
            padding: 10px 0;
            font-size: 1rem;
        }
        .button-container a {
            margin-left: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def create_db():
    conn = sqlite3.connect('contact_form_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(email, message):
    conn = sqlite3.connect('contact_form_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO submissions (email, message) VALUES (?, ?)", (email, message))
    conn.commit()
    conn.close()

if 'email' not in st.session_state:
    st.session_state['email'] = ''
if 'message' not in st.session_state:
    st.session_state['message'] = ''

st.markdown("<div class='main-header'>SOTA</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Study smarter with Odysseus - The Ultimate Study App</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.header("About Us")
st.write(
    """
    Welcome to SOTA, a pioneering startup dedicated to transforming the way people learn and grow. With our newest invention **Odysseus**, our innovative study app designed to help you navigate the seas of knowledge with ease and efficiency.
    
    With Odysseus, you can:
    
    1. **Capture Ideas**: Organize your thoughts with our smart note-taking system.
    2. **Visualize Concepts**: Create stunning mind maps to deepen understanding.
    3. **Connect and Share**: Engage with a thriving community of learners to exchange insights.
    4. **Master Content**: Use flashcards and other tools to enhance retention and ace your goals.
    
    At SOTA, we see learning as an **odyssey**—a journey of discovery, growth, and achievement. With Odysseus, we provide you with the tools to make every step of your journey purposeful and rewarding.
    """
)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.header("Features")
features = [
    "Note-Taking: Organize and save your notes efficiently.",
    "Mind Maps: Visualize your ideas and concepts easily.",
    "Flashcards: Create, review, and test your knowledge.",
    "Social Platform: Share and discover notes with a community of learners.",
]
for feature in features:
    st.markdown(f"<div class='feature-box'>{feature}</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.header("Contact Us")
with st.form("contact_form"):
    email = st.text_input("Your Email", placeholder="Enter your email", value=st.session_state['email'])
    message = st.text_area("Your Message", placeholder="Write your message here...", value=st.session_state['message'])
    submitted = st.form_submit_button("Send Message")

    if submitted:
        if not email or not message:
            st.error("Please fill out all fields.")
        else:
            st.session_state['email'] = email
            st.session_state['message'] = message
            try:
                save_to_db(email, message)
                st.success("Message successfully sent!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("<div class='button-container'>", unsafe_allow_html=True)
st.markdown(
    """
    <a href="https://www.yourcompanywebsite.com" class="link-button" target="_blank">Visit Company Website</a>
    <a href="https://www.yourapplicationwebsite.com" class="link-button" target="_blank" style="margin-left: 10px;">Try Odysseus Now</a>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='footer'>© 2024 SOTA. <a href='https://github.com/jmichikoleo'>GitHub</a></div>",
    unsafe_allow_html=True,
)

create_db()
