import re
import os
import requests
from textblob import TextBlob, Word

from CompassUTD.webscrape.text_extractor import (
    extract_course_description,
    extract_text_from_website,
)
from CompassUTD._secret import secrets


class _Secret:
    def __init__(self):
        if secrets:
            self.api_key = (secrets["GOOGLE_SEARCH_API"],)
            self.course_search_id = (secrets["COURSE_SEARCH_ID"],)
            self.degree_search_id = (secrets["DEGREE_SEARCH_ID"],)
            self.random_search_id = secrets["RANDOM_SEARCH_ID"]
        else:
            self.api_key = os.environ["GOOGLE_SEARCH_API"]
            self.course_search_id = os.environ["COURSE_SEARCH_ID"]
            self.degree_search_id = os.environ["DEGREE_SEARCH_ID"]
            self.random_search_id = os.environ["RANDOM_SEARCH_ID"]


class SearchCourse(_Secret):
    def _run(self, query: str):
        """_summary_

        Args:
            query (str): The query/term to do google search on catalog.utdallas.edu for courses.

        Returns:
            results (dict): JSON response containing link to the course, title, and snippet found in the search results
        """
        url = f"https://www.googleapis.com/customsearch/v1/siterestrict"
        params = {
            "key": self.api_key,
            "cx": self.course_search_id,
            "q": query,
            "fields": "spelling,items(link)",
            "num": 2,  # Number of results to return
        }
        data = requests.get(url, params=params).json()

        courses_extracted = []

        for course in data["items"]:
            course_link = course["link"]

            if not re.search(r"\d+$", course_link):
                # A valid course_link will have numbers at the tail
                data["items"].remove(course)
                continue

            # Get the 2-4 letter and 4 numbers code id from the link
            course_id = re.search(
                r"courses/([a-zA-Z]{2,4}\d{4})", course["link"]
            ).group(1)
            if not course_id in courses_extracted:
                # extract the content
                courses_extracted.append(course_id)
                course[course_id] = extract_course_description(course_id)
            del course["link"]

        return data


class SearchDegree(_Secret):
    def _run(self, query: str):
        """_summary_

        Args:
            query (str): The query/term to do google search on catalog.utdallas.edu for degree.

        Returns:
            results (dict): JSON response containing corrected spelling, link, title, and snippet of the degree results
        """
        url = f"https://www.googleapis.com/customsearch/v1/siterestrict"
        params = {
            "key": self.api_key,
            "cx": self.degree_search_id,
            "q": query,
            "fields": "spelling,items(link,title,snippet)",
            "num": 1,  # Number of results to return
        }
        data = requests.get(url, params=params).json()
        url = data["items"][0]["link"]
        text = extract_text_from_website(url=url)
        data["items"][0]["snippet"] = text
        del data["items"][0]["link"]
        return data


class SearchGeneral(_Secret):
    def _run(self, query: str):
        """_summary_

        Args:
            query (str): The query/term to do google search for.

        Returns:
            results (dict): JSON response containing corrected spelling, link, title, and snippet of the search results
        """
        url = f"https://www.googleapis.com/customsearch/v1/siterestrict"
        params = {
            "key": self.api_key,
            "cx": self.random_search_id,
            "q": query,
            "fields": "items(link)",
            "num": 1,  # Number of results to return
        }

        data = requests.get(url, params=params).json()
        for result in data["items"]:
            url = result["link"]
            try:
                text = extract_text_from_website(url=url)
                return {"data": text}
            except:
                continue


class SearchDefinition:
    def _run(self, query: str):
        sentence = TextBlob(query).correct()  # Spell check the query
        # Split the sentence into words
        words = sentence.words
        # Get the definition of each word
        result = {}
        for word in words:
            word = Word(word)
            result[word] = word.define() or None
        return result
