import requests
import json
from datetime import datetime, timedelta

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

today = datetime.utcnow().date()
tomorrow = today + timedelta(days=1)

url = f"https://api.football-data.org/v4/matches?dateFrom={today}&dateTo={tomorrow}"

headers = {
    "X-Auth-Token": API_KEY
}

response = requests.get(url, headers=headers)
data = response.json()

matches = []

for m in data.get("matches", []):

    if m["status"] != "FINISHED":

        matches.append({
            "home": m["homeTeam"]["name"],
            "away": m["awayTeam"]["name"]
        })

with open("data/matches_today.json","w") as f:
    json.dump(matches,f,indent=4)

print("Partite trovate:",len(matches))
