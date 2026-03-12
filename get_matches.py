import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("37ddec86e8578a1ff3127d5c394da749")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

# usa la data di oggi (semplice e compatibile con tutti i piani)
today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "date": today
}

response = requests.get(url, headers=headers, params=params)

print("HTTP STATUS:", response.status_code)

data = response.json()

print("API RESPONSE STATUS:", data.get("errors"), data.get("message"))

matches = []

for m in data.get("response", []):

    match = {
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "league": m["league"]["name"],
        "country": m["league"]["country"],
        "time": m["fixture"]["date"][11:16]
    }

    matches.append(match)

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, indent=2)

print("Partite trovate:", len(matches))