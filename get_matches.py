import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "date": today
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

# solo leghe affidabili
TOP_LEAGUES = [
39,   # Premier League
140,  # La Liga
135,  # Serie A
78,   # Bundesliga
61,   # Ligue 1
94,   # Primeira Liga
88,   # Eredivisie
253,  # MLS
2,    # Champions League
3     # Europa League
]

for match in data["response"]:

    league_id = match["league"]["id"]
    status = match["fixture"]["status"]["short"]

    # prendiamo solo partite NON iniziate
    if status != "NS":
        continue

    # filtriamo solo leghe top
    if league_id not in TOP_LEAGUES:
        continue

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    home_id = match["teams"]["home"]["id"]
    away_id = match["teams"]["away"]["id"]

    league = match["league"]["name"]
    country = match["league"]["country"]

    date = match["fixture"]["date"]

    matches.append({
        "home": home,
        "away": away,
        "home_id": home_id,
        "away_id": away_id,
        "league": league,
        "league_id": league_id,
        "country": country,
        "date": date
    })

print("Partite trovate:", len(matches))

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)