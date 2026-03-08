import requests
import os

API_KEY = os.getenv("37ddec86e8578a1ff3127d5c394da749")

print("API KEY:", API_KEY)

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "league": 135,
    "season": 2024
}

response = requests.get(url, headers=headers, params=params)

print("STATUS:", response.status_code)
print(response.text[:500])