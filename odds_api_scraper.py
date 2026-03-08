import requests
import json
import os

API_KEY = "b90932e65c14be06a870fd50fcd20ddc"

sports = [
"soccer_epl",
"soccer_italy_serie_a",
"soccer_spain_la_liga",
"soccer_germany_bundesliga",
"soccer_france_ligue_one"
]

all_odds = []

for sport in sports:

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

    params = {
        "apiKey": API_KEY,
        "regions": "eu",
        "markets": "totals",
        "oddsFormat": "decimal"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if isinstance(data, dict):
        continue

    for match in data:

        home = match.get("home_team")
        away = match.get("away_team")

        odds = {
            "over_1_5": None,
            "over_2_5": None,
            "over_3_5": None,
            "over_4_5": None
        }

        for bookmaker in match.get("bookmakers", []):

            for market in bookmaker.get("markets", []):

                if market["key"] == "totals":

                    for outcome in market["outcomes"]:

                        if outcome["name"] == "Over":

                            point = outcome["point"]
                            price = outcome["price"]

                            if point == 1.5:
                                odds["over_1_5"] = price

                            if point == 2.5:
                                odds["over_2_5"] = price

                            if point == 3.5:
                                odds["over_3_5"] = price

                            if point == 4.5:
                                odds["over_4_5"] = price

        all_odds.append({
            "home": home,
            "away": away,
            "odds": odds
        })

os.makedirs("quotes", exist_ok=True)

with open("quotes/odds_today.json", "w") as f:
    json.dump(all_odds, f, indent=4)

print("Quote salvate:", len(all_odds))
