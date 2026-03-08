import requests
import json
import os

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

sports = [
"soccer_italy_serie_a",
"soccer_epl",
"soccer_spain_la_liga",
"soccer_germany_bundesliga",
"soccer_france_ligue_one"
]

matches = []

for sport in sports:

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

    params = {
        "apiKey": API_KEY,
        "regions": "eu",
        "markets": "totals",
        "oddsFormat": "decimal"
    }

    r = requests.get(url, params=params)
    data = r.json()

    if isinstance(data, dict):
        continue

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
    json.dump(matches[:20], f, indent=4)

print("Partite con quote trovate:", len(matches))