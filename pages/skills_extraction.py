import streamlit as st
import google.generativeai as genai
import json
import PyPDF2


with st.sidebar:
    openai_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    uploaded_file = st.file_uploader("Resume", type=None, accept_multiple_files=False, key=None, help=None, on_change=None, disabled=False, label_visibility="visible")

st.title("💬 Skills Extraction Chatbot")

def extract_text_from_pdf():
    """Extracts text from each page of the given PDF and returns the complete text."""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    return ''.join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

start_message = "Welcome to Career Catalyst! Before we continue, we'd like to know a bit about you. Would you please describe your current career goals?"

if "messages" not in st.session_state:
    st.session_state["messages"] = [
            {"role": "model", "parts": [start_message]}
        ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["parts"][0])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your Gemini API key to continue.")
        st.stop()
    if not uploaded_file:
        st.info("Please add your resume to continue.")
        st.stop()
    if len(st.session_state.messages) == 1:
        st.session_state.messages.insert(0, {"role": "user", "parts": [f'''
             System Prompt: You are Career Catalyst, a master career coach. 
             Your current goal is to extract information from the person you're chatting with about their experience. 
             Ignore anything else they're talking about. Bring the conversation back to talking about their experience.
             Continue to ask deeper probing questions, extracting hard facts as much as possible.
             Here is the user's resume for additional context {extract_text_from_pdf()}
             ''']})
    st.chat_message("user").write(prompt)
    genai.configure(api_key=openai_api_key)

    model = genai.GenerativeModel('gemini-pro')
    st.session_state.messages.append({
        "role":"user",
        "parts":[prompt]
    })
    response = model.generate_content(st.session_state.messages).text
    st.session_state.messages.append({
        "role":"model",
        "parts":[response]
    })
    st.chat_message("model").write(response)