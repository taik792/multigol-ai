import requests
import json
import os
from datetime import datetime, timedelta, timezone

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

now = datetime.now(timezone.utc)

for m in data["response"]:

    status = m["fixture"]["status"]["short"]

    if status != "NS":
        continue

    match_time_str = m["fixture"]["date"]

    match_time = datetime.fromisoformat(match_time_str.replace("Z","+00:00"))

    if match_time - now < timedelta(hours=1):
        continue

    home = m["teams"]["home"]["name"]
    away = m["teams"]["away"]["name"]

    league = m["league"]["name"]
    country = m["league"]["country"]

    time = match_time.strftime("%H:%M")

    matches.append({
        "home": home,
        "away": away,
        "league": league,
        "country": country,
        "time": time
    })

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json","w") as f:
    json.dump(matches,f,indent=2)

print("Matches salvati:",len(matches))