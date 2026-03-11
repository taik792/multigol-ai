import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures?next=100"

headers = {
"x-apisports-key": API_KEY
}

response = requests.get(url, headers=headers)
data = response.json()

matches = []

for m in data["response"]:
    home = m["teams"]["home"]["name"]
    away = m["teams"]["away"]["name"]
    league = m["league"]["name"]
    time = m["fixture"]["date"][11:16]

    matches.append({
        "home": home,
        "away": away,
        "league": league,
        "time": time
    })

with open("data/matches_today.json","w") as f:
    json.dump(matches,f,indent=4)

print("Matches salvate:",len(matches))