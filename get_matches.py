import requests
import json
import os
from datetime import datetime, timedelta

API_KEY = os.getenv("37ddec86e8578a1ff3127d5c394da749")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")
tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")

dates = [today, tomorrow]

now = datetime.utcnow()
limit = now + timedelta(hours=24)

matches = []

for date in dates:

    params = {"date": date}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    for m in data.get("response", []):

        match_time = datetime.fromisoformat(m["fixture"]["date"].replace("Z",""))

        if now <= match_time <= limit:

            match = {
                "home": m["teams"]["home"]["name"],
                "away": m["teams"]["away"]["name"],
                "league": m["league"]["name"],
                "country": m["league"]["country"],
                "time": match_time.strftime("%H:%M")
            }

            matches.append(match)

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, indent=2)

print("Partite trovate:", len(matches))