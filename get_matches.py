import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "date": today
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

if "response" in data:
    for match in data["response"]:
        if match["fixture"]["status"]["short"] == "NS":
            matches.append({
                "fixture_id": match["fixture"]["id"],
                "league": match["league"]["name"],
                "country": match["league"]["country"],
                "home": match["teams"]["home"]["name"],
                "away": match["teams"]["away"]["name"],
                "date": match["fixture"]["date"]
            })

os.makedirs("data", exist_ok=True)

with open("data/matches.json", "w") as f:
    json.dump(matches, f)

print("Partite trovate:", len(matches))