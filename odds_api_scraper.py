import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/odds"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.now().strftime("%Y-%m-%d")

params = {
    "date": today
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

odds_dict = {}

for match in data.get("response", []):

    fixture_id = match["fixture"]["id"]

    for bookmaker in match.get("bookmakers", []):
        for bet in bookmaker.get("bets", []):

            if bet["name"] == "Goals Over/Under":

                over15 = None
                over25 = None

                for value in bet["values"]:
                    if value["value"] == "Over 1.5":
                        over15 = float(value["odd"])
                    if value["value"] == "Over 2.5":
                        over25 = float(value["odd"])

                if over15 and over25:
                    odds_dict[str(fixture_id)] = {
                        "over_1_5": over15,
                        "over_2_5": over25
                    }

# salva
with open("odds.json", "w") as f:
    json.dump(odds_dict, f, indent=2)

print("ODDS:", len(odds_dict))