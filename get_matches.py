import requests
import json
from datetime import datetime, timedelta

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

matches = []

for i in range(3):

    day = (datetime.utcnow() + timedelta(days=i)).strftime("%Y-%m-%d")

    params = {
        "date": day
    }

    response = requests.get(url, headers=headers, params=params)

    print("DATA:", day)
    print("HTTP STATUS:", response.status_code)

    data = response.json()

    if "response" in data:

        for m in data["response"]:

            if m["fixture"]["status"]["short"] == "NS":

                matches.append({
                    "home": m["teams"]["home"]["name"],
                    "away": m["teams"]["away"]["name"],
                    "league": m["league"]["name"],
                    "time": m["fixture"]["date"]
                })

print("Partite trovate:", len(matches))

with open("matches.json","w") as f:
    json.dump(matches,f,indent=4)