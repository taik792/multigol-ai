import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("37ddec86e8578a1ff3127d5c394da749")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "date": today,
    "status": "NS"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

for m in data.get("response", []):

    matches.append({
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "league": m["league"]["name"]
    })

matches = matches[:10]

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Matches found:", len(matches))
