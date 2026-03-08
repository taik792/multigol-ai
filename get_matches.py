import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"
BASE_URL = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

# data di oggi
today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "date": today
}

response = requests.get(BASE_URL, headers=headers, params=params)

data = response.json()

matches = []

if "response" in data:

    for match in data["response"]:

        status = match["fixture"]["status"]["short"]

        # SOLO PARTITE NON INIZIATE
        if status == "NS":

            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]

            league = match["league"]["name"]
            time = match["fixture"]["date"]

            matches.append({
                "league": league,
                "home": home,
                "away": away,
                "date": time
            })

# MAX 10 PARTITE
matches = matches[:10]

# salva file
with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Partite salvate:", len(matches))
