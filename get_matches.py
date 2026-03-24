import requests
import json
import os

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "next": 20,  # 🔥 PRENDE LE PROSSIME 20 PARTITE
    "timezone": "Europe/Rome"
}

response = requests.get(url, headers=headers, params=params)
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

# salva file
os.makedirs("data", exist_ok=True)

with open("data/matches.json", "w") as f:
    json.dump(matches, f, indent=2)

print("Matches trovati:", len(matches))