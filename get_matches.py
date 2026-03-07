import requests
import json
from datetime import datetime, timedelta

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

today = datetime.utcnow().date()
tomorrow = today + timedelta(days=1)

URL = f"https://api.football-data.org/v4/matches?dateFrom={today}&dateTo={tomorrow}"

headers = {
    "X-Auth-Token": API_KEY
}

response = requests.get(URL, headers=headers)
data = response.json()

if "matches" not in data:
    print("Errore API:", data)
    exit()

matches = data["matches"]

filtered = []

for m in matches:

    if m["status"] in ["SCHEDULED","TIMED"]:

        filtered.append({
            "home": m["homeTeam"]["name"],
            "away": m["awayTeam"]["name"],
            "date": m["utcDate"],
            "competition": m["competition"]["name"]
        })

with open("data/matches_today.json","w") as f:
    json.dump(filtered,f,indent=4)

print("Partite salvate:",len(filtered))
