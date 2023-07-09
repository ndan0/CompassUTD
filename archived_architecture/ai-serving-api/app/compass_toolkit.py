from dotenv import load_dotenv
import requests
import os

from typing import TYPE_CHECKING, List, Optional

from pydantic import Field

from langchain.tools.base import BaseTool
from langchain.agents.agent_toolkits.base import BaseToolkit

from langchain.callbacks.manager import CallbackManagerForToolRun

load_dotenv()

tool_microservice_url = str(os.getenv("TOOL_URL"))


class CompassToolkit(BaseToolkit):
    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            ProfessorSearchResults(),
            CoursesSearchResults(),
            DegreesSearchResults(),
            GeneralSearchResults(),
        ]


def request_error_handler(url: str, params={}) -> str:
    try:
        response = requests.get(url, params)
        response.raise_for_status()  # Raise an HTTPError if the status code is not in the 200 range
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(e)
        return e


class ProfessorSearchResults(BaseTool):
    name = "get_professor_rating_and_classes_taught"
    description = (
        "a search engine on professor of UT Dallas on RateMyProfessor database"
        "useful for when you need to answer questions about professors ratings, difficulty, and class taught."
        "will not return contact information, use the general_search tool for that."
        "Input should be a First, Last or Full name of the professor without greeting prefix"
        "Return will be full name, courses taught, overall rating, and difficulty rating"
    )

    def _run(
        self, name: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        url = f"https://{tool_microservice_url}/get-professor-rmp/{name}"
        return request_error_handler(url)

    async def _arun(
        self, name: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        raise NotImplementedError("does not support async yet")


class CoursesSearchResults(BaseTool):

    name = "course_search"
    description = (
        "a search engine on course database of UT Dallas"
        "useful for when you need to search for answer about courses."
        "Input should be a search query"
        "Return will be multiple results with course title and snippet"
    )

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        url = f"https://{tool_microservice_url}/get-possible-courses/{query}"
        return request_error_handler(url)

    async def _arun(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        raise NotImplementedError("does not support async yet")


class DegreesSearchResults(BaseTool):

    name = "college_degree_search"
    description = (
        "a search engine on college degree database of UT Dallas"
        "useful for when you need to search for answer about college degrees."
        "Input should be a search query"
        "Return will be multiple results with title, and snippet of the degree"
    )

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        url = f"https://{tool_microservice_url}/get-degree-info/{query}"
        return request_error_handler(url)

    async def _arun(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        raise NotImplementedError("does not support async yet")


class GeneralSearchResults(BaseTool):
    name = "general_utd_search"
    description = (
        "a search engine for general information about UT Dallas"
        "useful for when you need to search for answer related to professor(s), staff(s), school(s), department(s), and UT Dallas"
        "Searching for courses or college degrees are discouraged as there are better tools"
        "Input should be a search query"
        "Return will be multiple results with title, link and snippet"
    )

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        url = f"https://{tool_microservice_url}/search/{query}"
        return request_error_handler(url)

    async def _arun(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        raise NotImplementedError("does not support async yet")


class DictionaryRun(BaseTool):
    name = "get_definition_of_word"
    description = "a dictionary for simple word" "Input should be word or phrases"

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        url = f"https://{tool_microservice_url}/dictionary/{query}"
        return request_error_handler(url)

    async def _arun(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        url = f"https://{tool_microservice_url}/dictionary/{query}"
        return await request_error_handler(url)
