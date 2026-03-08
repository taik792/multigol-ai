import requests
import json
import os

API_KEY = os.getenv("b90932e65c14be06a870fd50fcd20ddc")

url = "https://api.the-odds-api.com/v4/sports/soccer/odds"

params = {
    "apiKey": API_KEY,
    "regions": "eu",
    "markets": "totals",
    "oddsFormat": "decimal"
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("Errore API")
    exit()

data = response.json()

matches = []

for game in data:

    home = game["home_team"]
    away = game["away_team"]

    over25 = None
    over35 = None

    for bookmaker in game.get("bookmakers", []):

        for market in bookmaker.get("markets", []):

            if market["key"] == "totals":

                for outcome in market["outcomes"]:

                    if outcome["name"] == "Over":

                        if outcome["point"] == 2.5:
                            over25 = outcome["price"]

                        if outcome["point"] == 3.5:
                            over35 = outcome["price"]

    if over25 and over35:

        matches.append({
            "home": home,
            "away": away,
            "over25": over25,
            "over35": over35
        })

os.makedirs("quotes", exist_ok=True)

with open("quotes/odds_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Partite trovate:", len(matches))
