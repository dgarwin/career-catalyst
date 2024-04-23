from io import BytesIO
import streamlit as st
import google.generativeai as genai
import json
from pdf2image import convert_from_bytes

with st.sidebar:
    openai_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
st.title("Resume Upload")
uploaded_file = st.file_uploader("Upload your resume", type=None, accept_multiple_files=False, key=None, help=None, on_change=None, disabled=False, label_visibility="visible")

if uploaded_file is not None:
    genai.configure(api_key=openai_api_key)
    model = genai.GenerativeModel('gemini-pro-vision')

    prompt = "Transcribe the contents of the resume."
    content = [prompt, convert_from_bytes(uploaded_file.getvalue())[0]]
    response = model.generate_content(
        content
    )
    st.write(response)


