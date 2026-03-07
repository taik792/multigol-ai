import json
import requests

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/odds"

headers = {
    "x-apisports-key": API_KEY
}

# leggiamo le partite
with open("data/matches_today.json") as f:
    matches = json.load(f)

odds = {}

for match in matches:

    home = match["home"]
    away = match["away"]

    params = {
        "bookmaker": "8",   # Bet365
        "league": "135",    # esempio Serie A
        "season": "2024"
    }

    response = requests.get(url, headers=headers, params=params)

    data = response.json()

    key = f"{home} vs {away}"

    quote = None

    for game in data.get("response", []):
        for bookmaker in game.get("bookmakers", []):
            for bet in bookmaker.get("bets", []):
                if bet["name"] == "Goals Over/Under":
                    quote = bet["values"][0]["odd"]

    odds[key] = {
        "multigol_2_4": quote
    }

with open("quotes/odds.json", "w") as f:
    json.dump(odds, f, indent=4)

print("Odds reali scaricate:", len(odds))
