import streamlit as st
import google.generativeai as genai

# --- 1. Configuration and Setup ---
# Configure the Gemini API using Streamlit secrets
api_key = st.secrets.get("GEMINI_API_KEY")

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

# --- 2. Streamlit App Setup ---
st.set_page_config(page_title="PyBricks Chatbot", layout="centered")
st.title("PyBricks Chatbot")
st.write("This chatbot helps you learn how to program LEGO robots with PyBricks.")

# --- 3. Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:  # Renamed for clarity
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# --- 4. Display Chat History ---
for msg in st.session_state.messages:
    st.markdown(f"**{msg['sender']}:** {msg['text']}")

# --- 5. User Input and Response Handling ---
user_input = st.text_input("Ask me anything about PyBricks:", st.session_state.user_input)

if st.button("Send") and user_input.strip():
    # Append user message to display
    st.session_state.messages.append({"sender": "You", "text": user_input})

    # Append user message to chat history in the correct format
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})

    try:
        # Get response from the model
        chat_session = model.start_chat(history=st.session_state.chat_history)
        response = chat_session.send_message(user_input)

        # Append model response to chat history in the correct format
        st.session_state.chat_history.append({"role": "model", "parts": [response.text]})

        # Append model response to display
        st.session_state.messages.append({"sender": "Chatbot", "text": response.text})

    except Exception as e:
        st.error(f"Error: {e}")

    # Clear user input
    st.session_state.user_input = ""

# --- 6. Reset Button ---
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.user_input = ""
