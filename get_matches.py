import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "date": today
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

if "response" in data:

    for match in data["response"]:

        status = match["fixture"]["status"]["short"]

        if status == "NS":

            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            league = match["league"]["name"]
            time = match["fixture"]["date"]

            matches.append({
                "home": home,
                "away": away,
                "league": league,
                "date": time
            })

matches = matches[:10]

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Partite salvate:", len(matches))