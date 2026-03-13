import requests
import json
import os

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "next": 300
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

for match in data["response"]:

    if match["fixture"]["status"]["short"] != "NS":
        continue

    matches.append({
        "home": match["teams"]["home"]["name"],
        "away": match["teams"]["away"]["name"],
        "home_id": match["teams"]["home"]["id"],
        "away_id": match["teams"]["away"]["id"],
        "league": match["league"]["name"],
        "country": match["league"]["country"],
        "league_id": match["league"]["id"],
        "date": match["fixture"]["date"]
    })

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print("Partite trovate:", len(matches))