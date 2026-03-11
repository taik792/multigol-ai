import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures?next=200"

headers = {
"x-apisports-key": API_KEY
}

response = requests.get(url, headers=headers)

data = response.json()

matches = []

for m in data["response"]:

match = {
    "home": m["teams"]["home"]["name"],
    "away": m["teams"]["away"]["name"],
    "league": m["league"]["name"],
    "time": m["fixture"]["date"][11:16]
}

matches.append(match)

with open("data/matches_today.json", "w") as f:
json.dump(matches, f, indent=4)

print("Partite salvate:", len(matches))