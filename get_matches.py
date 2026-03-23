import requests
import json
import os
from datetime import datetime

# 🔐 PRENDE API KEY CORRETTA
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise Exception("❌ API KEY non trovata!")

url = "https://v3.football.api-sports.io/fixtures"

today = datetime.utcnow().strftime("%Y-%m-%d")

query = {
    "date": today
}

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(url, headers=headers, params=query)
data = response.json()

matches = []

for m in data.get("response", []):
    status = m["fixture"]["status"]["short"]

    if status == "NS":
        matches.append(m)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print(f"✅ Scaricate {len(matches)} partite")