import requests

# Test Inference
url = "http://localhost:8000/inference/"
params = {
    "token": "z3ufvLWzBf7jaRys",
    "user_message": "What is the contact information for ECS advising?",
}

response = requests.post(url, params=params)
print(response)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error occurred while accessing URL.")
