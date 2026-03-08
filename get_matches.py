import requests
import json
from datetime import datetime, timedelta

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.today()
tomorrow = today + timedelta(days=1)

dates = [
    today.strftime("%Y-%m-%d"),
    tomorrow.strftime("%Y-%m-%d")
]

matches = []

for date in dates:

    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "date": date,
        "status": "NS"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    for game in data.get("response", []):

        home = game["teams"]["home"]["name"]
        away = game["teams"]["away"]["name"]

        matches.append({
            "home": home,
            "away": away
        })

with open("data/matches_today.json","w") as f:
    json.dump(matches,f,indent=4)

print("Partite trovate:",len(matches))
