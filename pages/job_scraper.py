import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Job Scraper")

with st.sidebar:
    jobs_to_search_var = st.text_input("Jobs to Serach for", key="jobs_to_search_key")

API_KEY = {search_api_key}
SEARCH_ENGINE_ID = {search_engine_id}

def google_search(query):
  query=f"site:jobs.lever.co {query}"
  url = "https://www.googleapis.com/customsearch/v1"
  params = {
    'key': API_KEY,
    'cx': SEARCH_ENGINE_ID,
    'q': query
  }
  response = requests.get(url, params=params)
  result = response.json()
  return result

def display_search_results(results):
  for item in results.get('items', []):
    title = item.get('title')
    snippet = item.get('snippet')
    link = item.get('link')
    st.write(f"### {title}\n{snippet}\n[Read more]({link})")

def scrape_jobs(results):
    for item in results.get('items', []):
        link = item.get('link')
        response=requests.get(link)
        if response.status_code==200:
            soup = BeautifulSoup(response.text, 'html.parser')
            job_header=soup.find_all(class_='posting-headline')
            job_description=soup.find_all(attrs={'data-qa': 'job-description'})
            if job_header:
                st.write(f"### {job_header[0].text}\n{job_description[0].text}\n[Read more]({link})")



if st.button('Scrape Jobs'):
    job_search_results=google_search(jobs_to_search_var)
    scrape_jobs(job_search_results)
        
