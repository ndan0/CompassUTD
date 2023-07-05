import dotenv
import requests
import os
import json

dotenv.load_dotenv()

class Tools:
    def __init__(self):
        self.tool_url = str(os.getenv('TOOL_URL'))
        
    def request_error_handler(self, url: str, params={}) -> str:
        try:
            response = requests.get(url, params)
            response.raise_for_status()  # Raise an HTTPError if the status code is not in the 200 range
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return e
    
    def result_to_natural_language(self, data: dict) -> str:
        num = 0
        str_result = "found these results:"
        num = 0
        for item in data["items"]:
            num += 1
            str_result += f"Item {num} with \"{item['title']}\" can be access at \"{item['link']}\", with snippet \"{item['snippet']}\"."
        return str_result
    
    def get_courses_from_query(self, query: str) -> str:
        url = f"https://{self.tool_url}/get-possible-courses/{query}"
        response = self.request_error_handler(url)
        #Turn the response into a natural language response
        return json.dumps(response)

    def get_degrees_from_query(self,query: str) -> str:
        url = f"https://{self.tool_url}/get-possible-degrees/{query}"
        response = self.request_error_handler(url)
        return json.dumps(response)
    
    def utdallas_search(self, query: str) -> str:
        url = f"https://{self.tool_url}/search/{query}"
        response = self.request_error_handler(url)
        return json.dumps(response)

    def access_utdallas_site(self, url_to_search: str) -> str:
        url = f"https://{self.tool_url}/access/"
        params = {
            "url": url_to_search
        }
        response = self.request_error_handler(url,params=params)
        try:
            return json.dumps(response)
        except:
            #Probably an error message
            return response
    
    def dictionary_search(self, query: str) -> str:
        url = f"https://{self.tool_url}/dictionary/{query}"
        response = self.request_error_handler(url)
        return json.dumps(response)
