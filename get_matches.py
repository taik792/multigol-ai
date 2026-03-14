import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

url = "https://www.flashscore.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

matches = []

games = soup.select(".event__match")

for g in games:

    home = g.select_one(".event__participant--home")
    away = g.select_one(".event__participant--away")

    if not home or not away:
        continue

    home = home.text.strip()
    away = away.text.strip()

    matches.append({

        "home": home,
        "away": away,
        "home_id": home,
        "away_id": away,

        "league": "Unknown",
        "league_id": 0,
        "country": "Unknown",

        "date": datetime.now().isoformat()

    })

print("Partite trovate:", len(matches))

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)