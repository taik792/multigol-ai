import requests
import json
from datetime import datetime, timedelta

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "X-Auth-Token": API_KEY
}

today = datetime.utcnow().date()
tomorrow = today + timedelta(days=1)

url = f"https://api.football-data.org/v4/matches?dateFrom={today}&dateTo={tomorrow}"

response = requests.get(url, headers=headers)
data = response.json()

matches = []

if "matches" in data:
    for m in data["matches"]:

        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        # prendiamo la data della partita
        match_date = m["utcDate"][:10]

        if match_date == str(today) or match_date == str(tomorrow):
            matches.append({
                "home": home,
                "away": away,
                "date": m["utcDate"],
                "competition": m["competition"]["name"]
            })

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Partite trovate:", len(matches))
