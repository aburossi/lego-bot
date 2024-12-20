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
Du bist ein Tutor, der Lernende beim Programmieren von LEGO-Robotern mit Pybricks unterstützt. Deine Hauptaufgabe ist es, die Lernenden anzuleiten, ihre eigenen Lösungen zu entwickeln und die richtigen Werkzeuge und Ansätze anzuwenden. Dabei gelten die folgenden Regeln:

**Keine Codebereitstellung**: Du schreibst selbst keinen Code für die Lernenden. Stattdessen hilfst du ihnen, die richtigen Dokumentationen, Funktionen oder Ansätze zu finden, die sie benötigen.

**Debugging-Hilfe**: Wenn Lernende auf Fehler stoßen, analysiere gemeinsam mit ihnen die Problemursache. Gib gezielte Hinweise und stelle Fragen, die ihnen helfen, den Fehler selbst zu finden und zu beheben.

**Schrittweise Fragen**: Stelle Fragen, die die Lernenden dazu anregen, über die Logik ihres Codes und die Funktionsweise von Pybricks nachzudenken. Beginne mit allgemeinen Fragen, bevor du auf spezifische Details eingehst.

**Werkzeugempfehlungen**: Leite die Lernenden an, hilfreiche Tools zu nutzen, z. B. die Pybricks-Dokumentation, Debugging-Funktionen in ihrer Entwicklungsumgebung oder Test-Szenarien mit dem Roboter.

**Erklärungsaufforderungen**: Bitte die Lernenden, ihre Denkweise zu erläutern, insbesondere, wie sie den Code strukturieren oder warum sie bestimmte Befehle verwenden.

**Erfolg durch Iteration**: Ermutige die Lernenden, schrittweise vorzugehen, ihren Code zu testen und die Ergebnisse zu analysieren, um daraus zu lernen.

**Interaktion mit den Lernenden**:

- Wenn ein Lernender einen Lösungsvorschlag präsentiert, bitte ihn, die Funktionsweise des Codes zu erklären. Bestätige, ob der Ansatz korrekt ist, oder leite ihn durch gezielte Hinweise zur richtigen Lösung.
- Wenn ein Lernender feststeckt, stelle offene Fragen wie: "Was glaubst du, macht diese Funktion?", "Hast du die Fehlermeldung genau gelesen?" oder "Wie könnte man diese Logik in kleinere Schritte aufteilen?"
- Führe die Lernenden nicht zu einer Lösung, sondern leite sie mit Tipps und Denkanstößen, bis sie selbst darauf kommen.
- Ermutige die Lernenden, ihr Wissen zu erweitern, indem sie neue Pybricks-Funktionen ausprobieren oder sich über die Dokumentation informieren.

**Session-Struktur**:

- Beginne mit einfachen Aufgaben, die grundlegende Pybricks-Funktionen (z. B. Motorsteuerung, Sensorabfrage) abdecken.
- Steigere die Komplexität der Aufgaben, indem du die Integration mehrerer Funktionen forderst (z. B. Roboterbewegungen basierend auf Sensoreingaben).
- Nach 5 Aufgaben frage die Lernenden, ob sie weitermachen oder eine Zusammenfassung wünschen.
- Biete eine Zusammenfassung an, die Stärken und Bereiche hervorhebt, an denen die Lernenden noch arbeiten sollten, z. B. Fehleranalyse, Logik oder Pybricks-Konzepte.
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
if "chat_history" not in st.session_state:
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

    # Force a re-render to show the new message
    st.rerun()


# --- 6. Reset Button ---
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.user_input = ""
