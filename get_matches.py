import requests
import json
from datetime import datetime, timedelta

API_URL = "https://api.football-data.org/v4/matches"
API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "X-Auth-Token": API_KEY
}

response = requests.get(API_URL, headers=headers)
data = response.json()

matches = data["matches"]

today = datetime.utcnow().date()
tomorrow = today + timedelta(days=1)

filtered_matches = []

for m in matches:

    status = m["status"]

    match_date = datetime.fromisoformat(
        m["utcDate"].replace("Z", "+00:00")
    ).date()

    if status != "FINISHED" and (match_date == today or match_date == tomorrow):

        filtered_matches.append({
            "home": m["homeTeam"]["name"],
            "away": m["awayTeam"]["name"],
            "date": m["utcDate"],
            "competition": m["competition"]["name"]
        })

with open("data/matches_today.json", "w") as f:
    json.dump(filtered_matches, f, indent=4)

print("Matches saved:", len(filtered_matches))
