import requests
import json
import os

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

SPORT = "soccer"
REGIONS = "eu"
MARKETS = "totals"
ODDS_FORMAT = "decimal"

URL = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"

params = {
    "apiKey": API_KEY,
    "regions": REGIONS,
    "markets": MARKETS,
    "oddsFormat": ODDS_FORMAT
}

response = requests.get(URL, params=params)
data = response.json()

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

    for bookmaker in match["bookmakers"]:

        for market in bookmaker["markets"]:

            if market["key"] == "totals":

                for outcome in market["outcomes"]:

                    name = outcome["name"]
                    point = outcome["point"]
                    price = outcome["price"]

                    if name == "Over":

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

with open("quotes/odds_today.json", "w") as f:
    json.dump(matches_odds, f, indent=4)

print("Quote salvate:", len(matches_odds))
