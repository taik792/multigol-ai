import requests
import json
from datetime import datetime, timedelta

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

now = datetime.utcnow()
tomorrow = now + timedelta(days=1)

params = {
    "from": now.strftime("%Y-%m-%d"),
    "to": tomorrow.strftime("%Y-%m-%d")
}

response = requests.get(url, headers=headers, params=params)

print("HTTP STATUS:", response.status_code)

data = response.json()

matches = []

if "response" in data:

    for m in data["response"]:

        status = m["fixture"]["status"]["short"]

        if status == "NS":

            matches.append({
                "home": m["teams"]["home"]["name"],
                "away": m["teams"]["away"]["name"],
                "league": m["league"]["name"],
                "time": m["fixture"]["date"]
            })

print("Partite trovate:", len(matches))

with open("matches.json", "w") as f:
    json.dump(matches, f, indent=4)