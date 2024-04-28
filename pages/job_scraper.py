import streamlit as st
import requests
from bs4 import BeautifulSoup
from google.cloud import storage

st.title("Job Scraper")

with st.sidebar:
    jobs_to_search_var = st.text_input("Jobs to Search for", key="jobs_to_search_key")
    custom_search_api_key=st.text_input("Custom search API Key", key="custom_search_api_key")
    search_engine_id=st.text_input("Search Engine ID", key="search_engine_id")

API_KEY = custom_search_api_key
SEARCH_ENGINE_ID = search_engine_id

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

import json
from google.cloud import storage

def push_to_bucket(bucket_name, destination_blob_name, job_header_string, job_description_string,job_link):
  # Create a storage client using default credentials
  client = storage.Client()
  
  # Get the bucket
  bucket = client.bucket(bucket_name)
  
  # Create a blob in the bucket at the specified path
  blob = bucket.blob(destination_blob_name)

  # Try to download the existing content, if any
  try:
    existing_data_json = blob.download_as_text()
    existing_data = json.loads(existing_data_json)
  except Exception as e:
    print(f"No existing data or unable to download: {str(e)}")
    existing_data = []

  # Prepare the new data to append
  new_data = {
    "job_header": job_header_string,
    "job_description": job_description_string,
    "job_link":job_link
  }

  # Append new data to the existing data
  if isinstance(existing_data, list):
    existing_data.append(new_data)
  else:
    existing_data = [existing_data, new_data]  # In case existing data isn't a list
  
  # Convert the combined data back to JSON
  final_json_data = json.dumps(existing_data)
  
  # Upload the combined JSON data
  blob.upload_from_string(final_json_data, content_type='application/json')
  
  # Optional: print statement to confirm upload
  print(f"File uploaded to {destination_blob_name}")

   

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
                push_to_bucket("job_scraper","heatlhcare_scrapper_data.json",job_header[0].text,job_description[0].text,link)





if st.button('Scrape Jobs'):
    job_search_results=google_search(jobs_to_search_var)
    scrape_jobs(job_search_results)
        