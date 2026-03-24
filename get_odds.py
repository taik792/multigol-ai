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

odds = {}

for item in data.get("response", []):
    fixture_id = str(item["fixture"]["id"])

    for book in item.get("bookmakers", []):
        for bet in book.get("bets", []):

            if bet["name"] == "Goals Over/Under":
                for v in bet["values"]:
                    if v["value"] == "Over 1.5":
                        odds.setdefault(fixture_id, {})["over_1_5"] = float(v["odd"])
                    if v["value"] == "Over 2.5":
                        odds.setdefault(fixture_id, {})["over_2_5"] = float(v["odd"])

os.makedirs("data", exist_ok=True)

with open("data/odds.json", "w") as f:
    json.dump(odds, f, indent=2)

print("Odds trovate:", len(odds))