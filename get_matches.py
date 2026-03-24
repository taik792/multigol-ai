import requests, json, os
from datetime import datetime, timedelta

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"
headers = {"x-apisports-key": API_KEY}

today = (datetime.utcnow() + timedelta(hours=2)).strftime("%Y-%m-%d")

params = {
    "date": today,
    "timezone": "Europe/Rome"
}

res = requests.get(url, headers=headers, params=params).json()

matches = []

for m in res.get("response", []):
    if m["fixture"]["status"]["short"] != "NS":
        continue

    matches.append({
        "fixture_id": m["fixture"]["id"],
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "date": m["fixture"]["date"],
        "league": m["league"]["name"]
    })

os.makedirs("data", exist_ok=True)

with open("data/matches.json", "w") as f:
    json.dump(matches, f, indent=2)

print("Matches:", len(matches))