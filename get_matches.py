import requests
import json
from datetime import datetime, timedelta

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

matches = []

# oggi + domani + dopodomani
for i in range(3):

    date = (datetime.utcnow() + timedelta(days=i)).strftime("%Y-%m-%d")

    params = {
        "date": date
    }

    r = requests.get(url, headers=headers, params=params)

    print("DATA:", date)
    print("HTTP STATUS:", r.status_code)

    data = r.json()

    if "response" in data:

        for m in data["response"]:

            matches.append({
                "home": m["teams"]["home"]["name"],
                "away": m["teams"]["away"]["name"],
                "league": m["league"]["name"],
                "time": m["fixture"]["date"]
            })

print("Partite trovate:", len(matches))

with open("matches.json","w") as f:
    json.dump(matches,f,indent=4)