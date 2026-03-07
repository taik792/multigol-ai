import requests
import json
import os
from datetime import datetime, timedelta

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

today = datetime.today().strftime('%Y-%m-%d')
tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

headers = {
    "x-apisports-key": API_KEY
}

matches = []

def get_fixtures(date):

    url = f"https://v3.football.api-sports.io/fixtures?date={date}"

    response = requests.get(url, headers=headers)
    data = response.json()

    if "response" not in data:
        return

    for game in data["response"]:

        home = game["teams"]["home"]["name"]
        away = game["teams"]["away"]["name"]
        league = game["league"]["name"]

        match_date = game["fixture"]["date"]

        matches.append({
            "date": match_date,
            "home": home,
            "away": away,
            "league": league,
            "home_goals_avg": 1.5,
            "away_goals_avg": 1.3,
            "home_conceded": 1.1,
            "away_conceded": 1.2
        })


get_fixtures(today)
get_fixtures(tomorrow)

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Matches aggiornati (oggi + domani)")
