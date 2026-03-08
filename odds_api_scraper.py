import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

url = "https://v3.football.api-sports.io/odds"

params = {
    "league": 39,
    "season": 2026
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

odds = {}

for match in data["response"]:

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    key = f"{home}-{away}"

    odds[key] = {}

    for bookmaker in match["bookmakers"]:

        for bet in bookmaker["bets"]:

            name = bet["name"]

            # 1X2
            if name == "Match Winner":

                for value in bet["values"]:

                    if value["value"] == "Home":
                        odds[key]["1"] = float(value["odd"])

                    if value["value"] == "Away":
                        odds[key]["2"] = float(value["odd"])

            # OVER/UNDER
            if name == "Goals Over/Under":

                for value in bet["values"]:

                    if value["value"] == "Over 2.5":
                        odds[key]["over25"] = float(value["odd"])

                    if value["value"] == "Under 2.5":
                        odds[key]["under25"] = float(value["odd"])

            # BTTS
            if name == "Both Teams Score":

                for value in bet["values"]:

                    if value["value"] == "Yes":
                        odds[key]["btts_yes"] = float(value["odd"])

with open("quotes/odds.json","w") as f:
    json.dump(odds,f,indent=4)

print("Quote salvate:",len(odds))
