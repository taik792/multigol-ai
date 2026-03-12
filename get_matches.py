import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "next": 200
}

response = requests.get(url, headers=headers, params=params)

print("HTTP STATUS:", response.status_code)

data = response.json()

matches = []

for m in data["response"]:

    if m["fixture"]["status"]["short"] == "NS":

        matches.append({
            "home": m["teams"]["home"]["name"],
            "away": m["teams"]["away"]["name"],
            "league": m["league"]["name"],
            "time": m["fixture"]["date"]
        })

print("Partite trovate:", len(matches))

with open("matches.json", "w") as f:
    json.dump(matches, f, indent=4)