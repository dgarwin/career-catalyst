import streamlit as st
import requests

import getpass
import os

import pathlib
import textwrap

import google.generativeai as genai
import PyPDF2
import pandas as pd


with st.sidebar:
    GOOGLE_API_KEY = st.text_input("Google API Key", key="GOOGLE_API_KEY")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    document_text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        if page_text:
            document_text += page_text
    return document_text

def chat_with_pdf_and_store_data(pdf_file,response_df):
    document_text = extract_text_from_pdf(pdf_file)

    questions = [
        "What is the user name, email, address and linkedin?",
        "Summarize user background in 3 sentences",
        "What are the jobs the user held with start date, end date and key experience in each position?",
        "What is the user background in terms of industry, length of experience?",
        "How many years of experience does the user have in which industries?",
        "What are the specific skills the user brings to the table?"
    ]

    responses = []  # Initialize list to store responses

    for question in questions:
        response = query_gemini(question, document_text)  # Pass document context
        responses.append(response)  # Store response in the list

    # Create a DataFrame to display questions and responses
    data = {"Question": questions, "Response": [response.text for response in responses]}
    response_df = pd.DataFrame(data)

    # Display the DataFrame in Markdown format in the notebook
    st.markdown(response_df.to_markdown(), unsafe_allow_html=True)

def query_gemini(question, document_context):
    # Create an instance of the Gemini LLM
    llm = genai.GenerativeModel('gemini-pro')

    # Combine user prompt and document context
    combined_input = f"{question} {document_context}"

    # Invoke the model with the combined input
    result = llm.generate_content(combined_input)

    # Extract and return the response from the result
    response = result
    return response

uploaded_resume = st.file_uploader("Upload your resume", type=None, accept_multiple_files=False, key=None, help=None, on_change=None, disabled=False, label_visibility="visible")

if st.button("Process Resumes"):
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("""Welcome to career coaching with Career Gemini.
                                          Career Gemini is a helpful agent to help you plan your career. Make the text shorter than 350 characters
                                          Make it sound helpful and intelligent. Ask the user to share the purpose of today's session.
                                          Make recommendation on suggested promtps like "plan a career pivot", "find a new job that fits my current profile" or
                                          "plan a long-term career advancement plan". """)
    except Exception as e:
        st.write("Google API Key error")
        st.stop()
    response_df = pd.DataFrame()
    resp=chat_with_pdf_and_store_data(uploaded_resume,response_df)
    


