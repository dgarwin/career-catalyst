import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Training Scraper")

with st.sidebar:
    jobs_to_search_var = st.text_input("Training to Search for", key="jobs_to_search_key")

API_KEY = "GOogle search API Key"
SEARCH_ENGINE_ID = "Search Key"

def google_search(query):
  query=f"site:udemy.com/course {query}"
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
            link = item.get('link')
            training_title=soup.find_all(attrs={'data-purpose': 'lead-title'})
            meta_price_tag = soup.find('meta', attrs={'property': 'udemy_com:price'})
            training_price=meta_price_tag['content']
            training_summary=soup.find_all(attrs={'data-purpose': 'lead-headline'})
            if training_title:
                st.write(f"### Training title: {training_title[0].text}\n Training Summary: {training_summary[0].text}\nTraining Price: {training_price}\n\n[Read more]({link})")



if st.button('Scrape Trainings'):
    job_search_results=google_search(jobs_to_search_var)
    scrape_jobs(job_search_results)
        
