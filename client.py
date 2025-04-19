import requests

data = {"location": "Seattle"}
response = requests.post("http://localhost:8000/weather", json=data)
print(response.json())