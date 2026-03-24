import requests
import json
import os

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}

params = {
    "next": 10
}

response = requests.get(url, headers=headers, params=params)

print("STATUS:", response.status_code)
print("TEXT:", response.text[:300])

data = response.json()

matches = []

for m in data.get("response", []):
    matches.append({
        "fixture_id": m["fixture"]["id"],
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "league": m["league"]["name"],
        "date": m["fixture"]["date"]
    })

os.makedirs("data", exist_ok=True)

with open("data/matches.json", "w") as f:
    json.dump(matches, f, indent=2)

print("Matches trovati:", len(matches))