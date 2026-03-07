import requests
import json

API_KEY = "b90932e65c14be06a870fd50fcd20ddc"

url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?regions=eu&markets=totals&apiKey={API_KEY}"

response = requests.get(url)
data = response.json()

odds = {}

for match in data:

    home = match["home_team"]
    away = match["away_team"]

    key = f"{home} vs {away}"

    odds[key] = {
        "multigol_2_4": 1.70
    }

with open("quotes/odds.json", "w") as f:
    json.dump(odds, f, indent=4)

print("Odds salvate:", len(odds))
