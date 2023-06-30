import os
from dotenv import load_dotenv
import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bs4 import BeautifulSoup

import requests


load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get-description/{course}")
def get_description(course: str):
    #Remove non-alphanumeric characters
    course = ''.join(e for e in course if e.isalnum())
    #Make a request to the course catalog
    response = requests.get(f"https://catalog.utdallas.edu/2023/undergraduate/courses/{course}")
    soup = BeautifulSoup(response.content, "html.parser")
    
    div_element = soup.find('div', id='bukku-page') #The description in <div id="bukku-page">
    combined_desc = ""
    if div_element:
        # Extract the text content from the div element
        combined_desc += div_element.text.strip()
    
    return {"description": combined_desc}
    
@app.get("/course-name-to-code/{name}")
def get_course_code(name: str):
    url = f"https://www.googleapis.com/customsearch/v1?key={os.getenv('GOOGLE_SEARCH_API')}&cx={os.getenv('COURSE_SEARCH_ID')}&q={name}"
    data = requests.get(url).json()
    search_items = data.get("items")
    print(search_items)
    links = []

    for i, search_item in enumerate(search_items, start=1):
        link = search_item.get("link")
        print("URL:", link, "\n")
        links.append(link)
        
    
    def extract_course_code(link):
        # Extract the course code from the link using regular expressions
        pattern = r"\/courses\/([a-zA-Z0-9]+)$"
        match = re.search(pattern, link)
        
        if match:
            course_code = match.group(1)
            return course_code
        else:
            return None
        
    course_codes = []
    for link in links:
        course_code = extract_course_code(link)
        if course_code and len(course_code) > 4:
            course_codes.append(course_code)

    return {"results": course_codes}
    

