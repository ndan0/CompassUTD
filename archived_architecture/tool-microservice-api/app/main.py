import io
import os
import re

import ratemyprofessor

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from textblob import TextBlob, Word

from text_extractor import ExtractTextFromURL, ExtractCourseInfo

import urllib3

urllib3.disable_warnings()
load_dotenv()

app = FastAPI()

UTDallas = ratemyprofessor.get_school_by_name("The University of Texas at Dallas")


@app.get("/get-possible-courses/{query}")
async def get_course_ids(query: str):
    """_summary_

    Args:
        query (str): The query/term to do google search on catalog.utdallas.edu for courses.

    Returns:
        results (dict): JSON response containing link to the course, title, and snippet found in the search results
    """
    url = f"https://www.googleapis.com/customsearch/v1/siterestrict"
    params = {
        "key": str(os.getenv("GOOGLE_SEARCH_API")),
        "cx": str(os.getenv("COURSE_SEARCH_ID")),
        "q": query,
        "fields": "items(link,title,snippet)",
        "num": 3,  # Number of results to return
    }
    data = requests.get(url, params=params).json()

    for course in data["items"]:
        # If the course link is not a link to a course, remove it from the list
        course_link = course["link"]
        # A valid course_link will have numbers at the tail
        if not re.search(r"\d+$", course_link):
            data["items"].remove(course)

    for course in data["items"]:
        # Get the 2-4 letter and 4 numbers code id from the link
        course_id = re.search(r"courses/([a-zA-Z]{2,4}\d{4})", course["link"]).group(1)
        course["snippet"] = ExtractCourseInfo(course_id)
        # Remove the link from the response
        del course["link"]

    return data


@app.get("/get-professor-rmp/{professor_name}")
async def get_professor_info(professor_name: str):
    """_summary_

    Args:
        professor_name (str): First, Last or Full Name of the professor

    Returns:
        dict: return full name, courses taught, overall rating, and difficulty rating
    """
    prof = ratemyprofessor.get_professor_by_school_and_name(UTDallas, professor_name)
    courses_taught = [course.name for course in prof.courses if course.count > 1]
    favor_rating = prof.rating
    difficulty_rating = prof.difficulty
    full_name = prof.name
    data = {
        "full_name": full_name,
        "courses_taught": courses_taught,
        "rate_my_professor_rating": {
            "overall_rating_out_of_5": favor_rating,
            "difficulty_rating_out_of_5": difficulty_rating,
        },
    }
    return data


@app.get("/get-degree-info/{query}")
async def degrees_search(query: str):
    """_summary_

    Args:
        query (str): The query/term to do google search on catalog.utdallas.edu for degree.

    Returns:
        results (dict): JSON response containing corrected spelling, link, title, and snippet of the degree results
    """
    url = f"https://www.googleapis.com/customsearch/v1/siterestrict"
    params = {
        "key": str(os.getenv("GOOGLE_SEARCH_API")),
        "cx": str(os.getenv("DEGREE_SEARCH_ID")),
        "q": query,
        "fields": "spelling,items(link,title,snippet)",
        "num": 1,  # Number of results to return
    }
    data = requests.get(url, params=params).json()
    url = data["items"][0]["link"]
    text = ExtractTextFromURL(url)
    data["items"][0]["snippet"] = text
    del data["items"][0]["link"]
    return data


@app.get("/search/{query}")
async def query_search(query: str):
    """_summary_

    Args:
        query (str): The query/term to do google search for.

    Returns:
        results (dict): JSON response containing corrected spelling, link, title, and snippet of the search results
    """
    url = f"https://www.googleapis.com/customsearch/v1/siterestrict"
    params = {
        "key": str(os.getenv("GOOGLE_SEARCH_API")),
        "cx": str(os.getenv("RANDOM_SEARCH_ID")),
        "q": query,
        "fields": "items(link)",
        "num": 5,  # Number of results to return
    }
    data = requests.get(url, params=params).json()
    for i in range(len(data["items"])):
        url = data["items"][0]["link"]
        try:
            text = ExtractTextFromURL(url)
            return {"data": text}
        except:
            continue


@app.get("/dictionary/{query}")
async def get_definition(query: str):
    sentence = TextBlob(query).correct()  # Spell check the query
    # Split the sentence into words
    words = sentence.words
    # Get the definition of each word
    result = {}
    for word in words:
        word = Word(word)
        result[word] = word.define() or None
    return result
