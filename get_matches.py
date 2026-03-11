import requests
import json
from datetime import datetime, timedelta

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

now = datetime.utcnow()

for m in data["response"]:

    status = m["fixture"]["status"]["short"]

    # solo partite non iniziate
    if status != "NS":
        continue

    match_time_str = m["fixture"]["date"]
    match_time = datetime.fromisoformat(match_time_str.replace("Z",""))

    # deve iniziare tra almeno 1 ora
    if match_time - now < timedelta(hours=1):
        continue

    home = m["teams"]["home"]["name"]
    away = m["teams"]["away"]["name"]
    league = m["league"]["name"]

    time = match_time.strftime("%H:%M")

    matches.append({
        "home": home,
        "away": away,
        "league": league,
        "time": time
    })

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print("Matches salvati:", len(matches))