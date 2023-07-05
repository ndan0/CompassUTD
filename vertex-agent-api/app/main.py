
import io
import os
import re

import fitz
import nltk
import requests
import vertexai
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from textblob import TextBlob, Word
from vertexai.language_models import TextGenerationModel

load_dotenv()

app = FastAPI()


vertexai.init(project="aerobic-gantry-387923", location="us-central1")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 512,
    "top_p": 0.9,
    "top_k": 40
}

model = TextGenerationModel.from_pretrained("text-bison@001")
    
@app.get("/get-possible-courses/{query}")
def get_course_ids(query: str):
    """_summary_

    Args:
        query (str): The query/term to do google search on catalog.utdallas.edu for courses.
        
    Returns:
        results (dict): JSON response containing link to the course, title, and snippet found in the search results
    """
    url = f"https://www.googleapis.com/customsearch/v1/siterestrict"
    params = {
        "key": str(os.getenv('GOOGLE_SEARCH_API')),
        "cx": str(os.getenv('COURSE_SEARCH_ID')),
        "q": query,
        "fields": "spelling,items(link,title,snippet)"
    }
    data = requests.get(url, params=params).json()

    for course in data["items"]:
        #If the course link is not a link to a course, remove it from the list
        course_link = course["link"]
        #A valid course_link will have numbers at the tail
        if not re.search(r'\d+$', course_link):
            data["items"].remove(course)
    return data

@app.get("/get-possible-degrees/{query}")
def degrees_search(query: str):
    """_summary_

    Args:
        query (str): The query/term to do google search on catalog.utdallas.edu for degree.

    Returns:
        results (dict): JSON response containing corrected spelling, link, title, and snippet of the degree results
    """
    url = f"https://www.googleapis.com/customsearch/v1/siterestrict"
    params = {
        "key": str(os.getenv('GOOGLE_SEARCH_API')),
        "cx": str(os.getenv('DEGREE_SEARCH_ID')),
        "q": query,
        "fields": "spelling,items(link,title,snippet)"
    }
    data = requests.get(url, params=params).json()
    
    return data

@app.get("/search/{query}")
def query_search(query: str):
    """_summary_

    Args:
        query (str): The query/term to do google search for.

    Returns:
        results (dict): JSON response containing corrected spelling, link, title, and snippet of the search results
    """
    url = f"https://www.googleapis.com/customsearch/v1/siterestrict"
    params = {
        "key": str(os.getenv('GOOGLE_SEARCH_API')),
        "cx": str(os.getenv('RANDOM_SEARCH_ID')),
        "q": query,
        "fields": "spelling,items(link,title,snippet)"
    }
    data = requests.get(url, params=params).json()
    return data

@app.get("/dictionary/{query}")
def get_definition(query:str):
    sentence = TextBlob(query).correct() #Spell check the query
    #Split the sentence into words
    words = sentence.words
    #Get the definition of each word
    result = {}
    for word in words:
        word = Word(word)
        result[word] = word.define() or None
    return result
    

@app.get("/access/")
async def access_url(request: Request):
    """_summary_

    Args:
        request (Request): JSON request containing the URL to access.

    Raises:
        ValueError: Invalid URL if the URL is not from utdallas.edu
        HTTPException: Error occurred while accessing URL.

    Returns:
        text data (str): content of the website in string format.
    """
    url = request.query_params.get("url")
    

    if not re.search(r"utdallas.edu", url):
        #Raise an error if the URL is not from utdallas.edu
        raise ValueError("Invalid URL")
    
    
    if re.search(r"catalog.utdallas.edu", url):
        #Check if the url contain catalog.utdallas.edu, then append /makepdf to the url to turn it into pdf

        if not re.search(r"makepdf", url):
            url += "/makepdf"
        
    response = requests.get(url)

    if not response:
        raise HTTPException(status_code=400, detail="Error occurred while accessing URL.")
    
    text = ""
    
    if response.headers.get("Content-Type") == "application/pdf":
        #Extract text from PDF
        pdf_file = io.BytesIO(response.content)
        with fitz.open(stream=pdf_file, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    else:
        #Extract text from HTML
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        
    #Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    #Remove underscores
    text = re.sub(r'_', '', text)
    
    return {"data": text}