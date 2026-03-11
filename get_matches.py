import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

today = datetime.utcnow().strftime("%Y-%m-%d")

headers = {
"x-apisports-key": API_KEY
}

params = {
"date": today
}

response = requests.get(url, headers=headers, params=params)

data = response.json()

matches = []

for m in data["response"]:

    home = m["teams"]["home"]["name"]
    away = m["teams"]["away"]["name"]

    league = m["league"]["name"]
    country = m["league"]["country"]

    time = m["fixture"]["date"][11:16]

    matches.append({
        "home":home,
        "away":away,
        "league":league,
        "country":country,
        "time":time
    })

with open("matches.json","w") as f:
    json.dump(matches,f,indent=2)

print("Partite salvate:",len(matches))