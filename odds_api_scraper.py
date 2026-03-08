import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

url = "https://v3.football.api-sports.io/odds"

response = requests.get(url, headers=headers)
data = response.json()

odds = {}

for game in data["response"]:

    home = game["teams"]["home"]["name"]
    away = game["teams"]["away"]["name"]

    key = f"{home}-{away}"

    over25 = None
    under25 = None

    for bookmaker in game["bookmakers"]:

        for bet in bookmaker["bets"]:

            if bet["name"] == "Goals Over/Under":

                for value in bet["values"]:

                    if value["value"] == "Over 2.5":
                        over25 = float(value["odd"])

                    if value["value"] == "Under 2.5":
                        under25 = float(value["odd"])

    if over25:

        odds[key] = {
            "over25": over25,
            "under25": under25
        }

with open("quotes/odds.json","w") as f:
    json.dump(odds,f,indent=4)

print("Quote bookmaker trovate:",len(odds))
