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
    generation_config=
