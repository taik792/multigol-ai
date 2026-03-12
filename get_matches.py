import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

# leghe principali
leagues = [39, 135, 140, 78, 61]

matches = []

for league in leagues:

    params = {
        "league": league,
        "season": 2025,
        "status": "NS"
    }

    response = requests.get(url, headers=headers, params=params)

    print("LEAGUE:", league)
    print("HTTP STATUS:", response.status_code)

    data = response.json()

    for m in data.get("response", []):

        matches.append({
            "home": m["teams"]["home"]["name"],
            "away": m["teams"]["away"]["name"],
            "league": m["league"]["name"],
            "time": m["fixture"]["date"],
            "home_id": m["teams"]["home"]["id"],
            "away_id": m["teams"]["away"]["id"]
        })

print("Partite trovate:", len(matches))

with open("matches.json", "w") as f:
    json.dump(matches, f, indent=4)