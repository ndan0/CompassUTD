from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bs4 import BeautifulSoup
from matching import FuzzyMatch
import requests


Courses = FuzzyMatch("courses.csv", "name", "code")

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
    return {"result": Courses.match(name)}
    

