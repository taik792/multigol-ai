import requests
import json

API_KEY = "LA_TUA_API_KEY"

url = "https://v3.football.api-sports.io/fixtures?next=50"

headers = {
    "x-apisports-key": API_KEY
}

res = requests.get(url, headers=headers).json()

matches = []

for match in res["response"]:
    matches.append({
        "fixture": {
            "id": match["fixture"]["id"],
            "date": match["fixture"]["date"]
        },
        "teams": {
            "home": {"name": match["teams"]["home"]["name"]},
            "away": {"name": match["teams"]["away"]["name"]}
        },
        "league": {
            "name": match["league"]["name"]
        }
    })

with open("data/matches.json", "w") as f:
    json.dump(matches, f, indent=2)

print("Matches salvati:", len(matches))