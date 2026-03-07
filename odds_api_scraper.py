import json
import requests

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

# leggiamo le partite trovate prima
with open("data/matches_today.json") as f:
    matches = json.load(f)

odds = {}

url = "https://v3.football.api-sports.io/odds"

response = requests.get(url, headers=headers)
data = response.json()

for match in matches:

    home = match["home"]
    away = match["away"]

    key = f"{home} vs {away}"

    quote = None

    for game in data.get("response", []):
        if "bookmakers" in game:
            for bookmaker in game["bookmakers"]:
                for bet in bookmaker["bets"]:
                    if bet["name"] == "Goals Over/Under":
                        quote = bet["values"][0]["odd"]

    odds[key] = {
        "multigol_2_4": quote
    }

with open("quotes/odds.json", "w") as f:
    json.dump(odds, f, indent=4)

print("Odds scaricate:", len(odds))
