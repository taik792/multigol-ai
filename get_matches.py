import requests
import os

API_KEY = os.getenv("37ddec86e8578a1ff3127d5c394da749")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "next": 10
}

response = requests.get(url, headers=headers, params=params)

print("HTTP STATUS:", response.status_code)
print("RISPOSTA API:")
print(response.text)