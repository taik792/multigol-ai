import requests
import json
from datetime import datetime

API_KEY = "YOUR_API_KEY"  # NON serve se usi secrets in GitHub

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime('%Y-%m-%d')

params = {
    "date": today
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

for fixture in data.get("response", []):
    matches.append({
        "fixture_id": fixture["fixture"]["id"],
        "home": fixture["teams"]["home"]["name"],
        "away": fixture["teams"]["away"]["name"],
        "date": fixture["fixture"]["date"],
        "league": fixture["league"]["name"],
        "country": fixture["league"]["country"]
    })

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print(f"✅ Salvate {len(matches)} partite")