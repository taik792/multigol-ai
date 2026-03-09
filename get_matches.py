import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.now().strftime("%Y-%m-%d")

params = {
    "date": today,
    "timezone": "Europe/Rome"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

allowed_leagues = [
    "Serie A",
    "Serie B",
    "Premier League",
    "Championship",
    "La Liga",
    "Segunda División",
    "Bundesliga",
    "2. Bundesliga",
    "Ligue 1",
    "Ligue 2",
    "Eredivisie",
    "Primeira Liga",
    "MLS",
    "UEFA Champions League",
    "UEFA Europa League",
    "UEFA Europa Conference League"
]

matches = []

for match in data["response"]:

    league = match["league"]["name"]

    if league in allowed_leagues:

        status = match["fixture"]["status"]["short"]

        if status in ["NS","TBD"]:

            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]

            date = match["fixture"]["date"]

            dt = datetime.fromisoformat(date.replace("Z",""))

            match_date = dt.strftime("%d-%m-%Y")
            match_time = dt.strftime("%H:%M")

            matches.append({
                "home": home,
                "away": away,
                "league": league,
                "date": match_date,
                "time": match_time
            })

with open("matches.json","w",encoding="utf-8") as f:
    json.dump(matches,f,indent=4,ensure_ascii=False)

print("Partite salvate:",len(matches))
