import requests
import json
import os

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
 "x-apisports-key": API_KEY
}

params = {
 "next": 200
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

for m in data["response"]:

    if m["fixture"]["status"]["short"] != "NS":
        continue

    matches.append({
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "home_id": m["teams"]["home"]["id"],
        "away_id": m["teams"]["away"]["id"],
        "league": m["league"]["name"],
        "country": m["league"]["country"],
        "league_id": m["league"]["id"],
        "date": m["fixture"]["date"]
    })

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print("Partite trovate:", len(matches))