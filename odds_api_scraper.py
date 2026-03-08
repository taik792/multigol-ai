import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

with open("data/matches_today.json") as f:
    matches = json.load(f)

odds_data = {}

for match in matches:

    fixture = match["fixture_id"]

    url = "https://v3.football.api-sports.io/odds"

    params = {
        "fixture": fixture
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if not data["response"]:
        continue

    bookmakers = data["response"][0]["bookmakers"][0]["bets"]

    odds = {}

    for bet in bookmakers:

        if bet["name"] == "Goals Over/Under":

            for value in bet["values"]:

                odds[value["value"]] = float(value["odd"])

    odds_data[match["home"] + " vs " + match["away"]] = odds

with open("quotes/odds.json", "w") as f:
    json.dump(odds_data, f, indent=4)

print("Quote salvate")
