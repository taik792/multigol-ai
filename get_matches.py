import requests
import json
import os
from datetime import datetime

# INSERISCI QUI LA TUA API KEY
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

for m in data["response"]:

    status = m["fixture"]["status"]["short"]

    # Prende solo partite non iniziate
    if status != "NS":
        continue

    home = m["teams"]["home"]["name"]
    away = m["teams"]["away"]["name"]
    league = m["league"]["name"]

    time = m["fixture"]["date"][11:16]

    matches.append({
        "home": home,
        "away": away,
        "league": league,
        "time": time
    })

# crea cartella data se non esiste
os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print("Matches salvati:", len(matches))
