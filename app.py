import os
import streamlit as st
import google.generativeai as genai

# Configure the Gemini API using Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    st.error("GEMINI_API_KEY not set in Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Define system instructions
system_instructions = """
Du bist ein Tutor, der Lernende beim Programmieren von LEGO-Robotern mit PyBricks unterstützt. ...
"""

# Initialize the Generative Model
model = genai.GenerativeModel(
    model_name="learnlm-1.5-pro-experimental",
    generation_config={
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    },
    system_instruction=system_instructions,
)

# Streamlit App
st.set_page_config(page_title="PyBricks Chatbot", layout="centered")
st.title("PyBricks Chatbot")
st.write("This chatbot helps you learn how to program LEGO robots with PyBricks.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Display chat history
for msg in st.session_state.messages:
    st.markdown(f"**{msg['sender']}:** {msg['text']}")

# Input box
user_input = st.text_input("Ask me anything about PyBricks:", st.session_state.user_input)

if st.button("Send") and user_input.strip():
    # Append user message
    st.session_state.messages.append({"sender": "You", "text": user_input})
    st.session_state.history.append({"author": "User", "content": user_input})

    try:
        # Get response from the model
        chat_session = model.start_chat(history=st.session_state.history)
        response = chat_session.send_message(user_input)

        # Append model response
        st.session_state.history.append({"author": "Model", "content": response.text})
        st.session_state.messages.append({"sender": "Chatbot", "text": response.text})
    except Exception as e:
        st.error(f"Error: {e}")

    # Clear user input
    st.session_state.user_input = ""  # Reset the input field

# Reset button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.history = []
    st.session_state.user_input = ""  # Clear the input field
