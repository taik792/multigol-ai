import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.now().strftime("%Y-%m-%d")

params = {
    "date": today,
    "timezone": "Europe/Rome"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

if "response" in data:

    for match in data["response"]:

        status = match["fixture"]["status"]["short"]

        # prendiamo solo partite non iniziate
        if status in ["NS", "TBD"]:

            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]

            matches.append({
                "home": home,
                "away": away
            })

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, indent=4, ensure_ascii=False)

print("Partite salvate:", len(matches))
