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

start_message = """Welcome to Career Catalyst! We are here to support you in discovering the career that has you fulfilled. If you could have anything in your career, what would it be?

Before we begin, please also enter your resume on the left tool bar."""
st.chat_message('coach').write(start_message)
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

questions = [
    "where do you want to be in 10 years?",
    'what does your life styel look like and how does your career support this?',
    'what are your monetary goals?',
    'what industry do you want to be in?'
]

base_prompt = '''
             You are a career coach. You are here to support the user in discovering a career that has them fulfilled. 
             You are biased towards not offering advice, and tend to ask open-ended questions to get the candidate to examine what they want.  
             You have the candidate's prior experience from a resume below.

             Ask the user an open-ended question on what they want out of their career. Avoid directly referencing the information in their resume.
             Start with open-ended questions and progress to more specific questions. 

             chat history: {chat_history}
             resume: {resume}
             question:
             '''

genai.configure(api_key=openai_api_key)
model = genai.GenerativeModel('gemini-pro')

if "coach" not in st.session_state:
        st.session_state["coach"] = "career catalyst"
        st.chat_message('coach').write(start_message)

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your Gemini API key to continue.")
        st.stop()
    if not uploaded_file:
        st.info("Please add your resume to continue.")
        st.stop()
    
    st.chat_message("user").write(prompt)
    


    
    

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })
    response = model.generate_content(
        base_prompt.format(
            chat_history = st.session_state.messages, 
            resume = extract_text_from_pdf())
            ).text
    st.session_state.messages.append({
        "role":"coach",
        "content":response
    })

   