import requests

url = "http://127.0.0.1:8000/access/"
#params = {"url": "https://dox.utdallas.edu/syl120000"}
#params = {"url": "https://catalog.utdallas.edu/2018/undergraduate/courses/cs1336"}
#params = {"url": "https://catalog.utdallas.edu/2023/undergraduate/home"}
params = {"url": "https://catalog.utdallas.edu/2022/undergraduate/courses/math2419/makepdf"}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json().get("data")
    print(data)
else:
    print("Error occurred while accessing URL.")