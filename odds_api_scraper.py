import json
import requests
from datetime import datetime

API_KEY = "b90932e65c14be06a870fd50fcd20ddc"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.today().strftime('%Y-%m-%d')

url = "https://v3.football.api-sports.io/odds"

params = {
    "date": today
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

odds = {}

for game in data.get("response", []):

    home = game["teams"]["home"]["name"]
    away = game["teams"]["away"]["name"]

    key = f"{home} vs {away}"

    quote = None

    for bookmaker in game.get("bookmakers", []):
        for bet in bookmaker.get("bets", []):

            if bet["name"] == "Goals Over/Under":

                for value in bet["values"]:

                    if value["value"] == "Over 2.5":
                        quote = value["odd"]

    odds[key] = {
        "multigol_2_4": quote
    }

with open("quotes/odds.json", "w") as f:
    json.dump(odds, f, indent=4)

print("Odds scaricate:", len(odds))
