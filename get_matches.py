import requests
import json
from datetime import datetime, timedelta

API_KEY = "37ddec86e8578a1ff3127d5c394da749"
URL = "https://api.football-data.org/v4/matches"

headers = {
    "X-Auth-Token": API_KEY
}

response = requests.get(URL, headers=headers)

data = response.json()

# controllo sicurezza
if "matches" not in data:
    print("ERRORE API:")
    print(data)
    exit()

matches = data["matches"]

today = datetime.utcnow().date()
tomorrow = today + timedelta(days=1)

filtered = []

for m in matches:

    status = m["status"]

    match_date = datetime.fromisoformat(
        m["utcDate"].replace("Z","+00:00")
    ).date()

    if status != "FINISHED" and (match_date == today or match_date == tomorrow):

        filtered.append({
            "home": m["homeTeam"]["name"],
            "away": m["awayTeam"]["name"],
            "date": m["utcDate"],
            "competition": m["competition"]["name"]
        })

with open("data/matches_today.json","w") as f:
    json.dump(filtered,f,indent=4)

print("Partite salvate:",len(filtered))
