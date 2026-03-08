import requests
import json
import os

API_KEY = "37ddec86e8578a1ff3127d5c394da749"
URL = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"

params = {
    "apiKey": API_KEY,
    "regions": "eu",
    "markets": "totals",
    "oddsFormat": "decimal"
}

response = requests.get(URL, params=params)

data = response.json()

# controllo errore API
if isinstance(data, dict) and "message" in data:
    print("Errore API:", data["message"])
    exit()

matches_odds = []

for match in data:

    home = match["home_team"]
    away = match["away_team"]

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

    matches_odds.append({
        "home": home,
        "away": away,
        "odds": odds
    })

os.makedirs("quotes", exist_ok=True)

with open("quotes/odds_today.json", "w") as f:
    json.dump(matches_odds, f, indent=4)

print("Quote salvate:", len(matches_odds))