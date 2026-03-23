import requests
import json
from datetime import datetime

API_KEY = "YOUR_API_KEY"

url = "https://v3.football.api-sports.io/fixtures?date=" + datetime.utcnow().strftime("%Y-%m-%d")

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(url, headers=headers)
data = response.json()

matches = []

for fixture in data["response"]:
    status = fixture["fixture"]["status"]["short"]

    # SOLO PARTITE NON INIZIATE
    if status not in ["NS"]:
        continue

    match_data = {
        "fixture_id": fixture["fixture"]["id"],
        "home": fixture["teams"]["home"]["name"],
        "away": fixture["teams"]["away"]["name"],
        "date": fixture["fixture"]["date"],
        "league": fixture["league"]["name"],
        "country": fixture["league"]["country"]
    }

    matches.append(match_data)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print(f"✅ Matches salvate: {len(matches)}")