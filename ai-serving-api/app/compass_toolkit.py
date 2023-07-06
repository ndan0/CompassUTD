from dotenv import load_dotenv
import requests
import os

from typing import TYPE_CHECKING, List

from pydantic import Field

from langchain.tools.base import BaseTool
from langchain.agents.agent_toolkits.base import BaseToolkit

load_dotenv()

tool_microservice_url = str(os.getenv('TOOL_URL'))

class CompassToolKit(BaseToolKit):
    def get_tools(self): -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            CoursesSearchRun(),
            CollegeDegreesRun(),
            GeneralSearchRun(),
            ExtractTextRun(),
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

class CoursesSearchRun(BaseTool):

    name = "course_search"
    description = (
        "a search engine on course database of UT Dallas"
        "useful for when you need to answer questions about courses."
        "Input should be a search query"
        "Return will be multiple results with title, link and snippet"
    )

    def _run(
             query: str,
             run_manager: Optional[CallbackManagerForToolRun] = None
    ): -> str:
        url = f"https://{tool_microservice_url}/get-possible-courses/{query}"
        return request_error_handler(url)

    async def _arun(
                    query: str,
                    run_manager: Optional[CallbackManagerForToolRun] = None
    ): -> str:
        url = f"https://{tool_microservice_url}/get-possible-courses/{query}"
        return (await request_error_handler(url))


class CollegeDegreesRun(BaseTool):

    name = "college_degree_search"
    description = (
        "a search engine on college degree database of UT Dallas"
        "useful for when you need to answer questions about college degree like majors, minors, concentration,certifications."
        "Input should be a search query"
        "Return will be multiple results with title, link and snippet"
    )

    def _run(
             query: str,
             run_manager: Optional[CallbackManagerForToolRun] = None
    ): -> str:
        url = f"https://{tool_microservice_url}/get-possible-degrees/{query}"
        return request_error_handler(url)

    async def _arun(
                    query: str,
                    run_manager: Optional[CallbackManagerForToolRun] = None
    ): -> str:
        url = f"https://{tool_microservice_url}/get-possible-degrees/{query}"
        return (await request_error_handler(url))

class GeneralSearchRun(BaseTool):
    name = "general_search"
    description = (
        "a search engine for general information about UT Dallas"
        "useful for when you need to answer question related to professor(s), staff(s), school(s), department(s), and UT Dallas"
        "Searching for courses or college degrees are discouraged as there are better tools"
        "Input should be a search query"
        "Return will be multiple results with title, link and snippet"
    )
    def _run(
             query: str,
             run_manager: Optional[CallbackManagerForToolRun] = None
    ): -> str:
        url = f"https://{tool_microservice_url}/search/{query}"
        return request_error_handler(url)

    async def _arun(
                    query: str,
                    run_manager: Optional[CallbackManagerForToolRun] = None
    ): -> str:
        url = f"https://{tool_microservice_url}/search/{query}"
        return (await request_error_handler(url))

class ExtractTextRun(BaseTool):
    name = "extract_text_from_website"
    description = (
        "a text extractor from any UT Dallas website"
        "useful for when you need to find more information about when the snippet content is not enough"
        "Input should be a utdallas.edu link/url"
        "return will be text extracted from the website"
    )
    def _run(
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ): -> str:
        url = f"https://{tool_microservice_url}/access/"
        params = {
            "url": url_to_search
        }
        response = request_error_handler(url,params=params)
        try:
            return response["data"]
        except:
            #Probably an error message
            return "The site unable to access at this time."

    async def _arun(
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ): -> str:
        url = f"https://{tool_microservice_url}/access/"
        params = {
            "url": url_to_search
        }
        response = awaitrequest_error_handler(url,params=params)
        try:
            return response["data"]
        except:
            #Probably an error message
            return "The site unable to access at this time."

class DictionaryRun(BaseTool):
    name = "get_definition_of_word"
    description = (
        "a dictionary for simple word"
        "Input should be word or phrases"
    )
    def _run(
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ): -> str:
        url = f"https://{tool_microservice_url}/dictionary/{query}"
        return request_error_handler(url)

    async def _arun(
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ): -> str:
        url = f"https://{tool_microservice_url}/dictionary/{query}"
        return (await request_error_handler(url))










