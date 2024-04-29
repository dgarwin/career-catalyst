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

uploaded_resume = st.file_uploader("Upload your resume", type=None, accept_multiple_files=False, key=None, help=None, on_change=None, disabled=False, label_visibility="visible")

if st.button("Process Resumes"):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("""Welcome to career coaching with Career Gemini.
    Career Gemini is a helpful agent to help you plan your career. Make the text shorter than 350 characters
    Make it sound helpful and intelligent. Ask the user to share the purpose of today's session.
    Make recommendation on suggested promtps like "plan a career pivot", "find a new job that fits my current profile" or
    "plan a long-term career advancement plan". """)

