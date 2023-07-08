import requests

# Test Access
# url = "http://127.0.0.1:8000/access/"
# params = {"url": "https://dox.utdallas.edu/syl120000"}
# params = {"url": "https://catalog.utdallas.edu/2018/undergraduate/courses/acct2302"}
# params = {"url": "https://catalog.utdallas.edu/2023/undergraduate/home"}
# params = {"url": "https://catalog.utdallas.edu/2022/undergraduate/courses/hist2301"}
# params = {"url": "https://engineering.utdallas.edu/academics/undergraduate-majors/undergrad-advising/ecs-advisors/"}
# params = {"url": "https://jindal.utdallas.edu/advising/"}

# response = requests.get(url, params=params)

# Test Inference
url = "http://localhost:80/inference/"
params = {
    "token": "z3ufvLWzBf7jaRys",
    "user_message": "Nice, where is his office?",
}

response = requests.post(url, params=params)
print(response)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error occurred while accessing URL.")
