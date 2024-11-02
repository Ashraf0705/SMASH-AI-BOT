import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-pro"
PAGE_TITLE = " 👁️SMASH👁️  AI ASSISTANT"
USER_ROLE, ASSISTANT_ROLE = "User", "Gemini Pro"

# Configure Streamlit page settings
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=":brain:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize the model
gen_ai.configure(api_key=API_KEY)
model = gen_ai.GenerativeModel(MODEL_NAME)

# Sidebar for model settings and theme
st.sidebar.header("Settings")
st.sidebar.subheader("Model & Interface")
theme = st.sidebar.radio("Choose Theme", ("Light", "Dark"))
st.sidebar.markdown("---")

# Custom styling based on theme
if theme == "Dark":
    st.markdown("""
        <style>
            .stApp {background-color: #0d1117; color: #c9d1d9;}
            .stTextArea {background-color: #161b22; color: #c9d1d9;}
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            .stApp {background-color: #ffffff; color: #000000;}
        </style>
        """, unsafe_allow_html=True)

# Function to initialize chat session in Streamlit if not already present
def initialize_chat():
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.message_count = 0

# Display chat history
def display_chat_history():
    st.subheader("Chat History")
    for i, message in enumerate(st.session_state.chat_session.history):
        role = ASSISTANT_ROLE if message.role == "model" else USER_ROLE
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

# Function to process user input and get model response
def process_input(user_input):
    if user_input:
        st.session_state.message_count += 1
        st.chat_message(USER_ROLE).markdown(user_input)

        try:
            response = st.session_state.chat_session.send_message(user_input)
            with st.chat_message(ASSISTANT_ROLE):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Failed to get response: {e}")

# Display page title, settings, and message count
st.title(PAGE_TITLE)
initialize_chat()

# Display chat history
st.expander("Conversation", expanded=True).write(display_chat_history())

# Display message input field and feedback section
st.metric("Messages Sent", st.session_state.message_count)
feedback = st.radio("Rate Response:", ["👍", "👎"], index=1)
st.write(f"Your feedback: {feedback}")

# Place the input outside of any restricted containers
user_input = st.chat_input("Type your message and hit Enter!")
process_input(user_input)

# Add a feedback prompt after every 5 messages
if st.session_state.message_count > 0 and st.session_state.message_count % 5 == 0:
    st.balloons()
    st.info("You've reached 5 messages! Please consider sharing your feedback on Gemini Pro.")
