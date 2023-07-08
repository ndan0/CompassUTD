import requests

# Test Inference
url = "http://localhost:80/inference/"
params = {
    "token": "z3ufvLWzBf7jaRys",
    "user_message": "Compare Math 2413 to Math 2417",
}

response = requests.post(url, params=params)
print(response)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error occurred while accessing URL.")
