import requests
import json
import os

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://api.the-odds-api.com/v4/sports/soccer/odds"

params = {
    "apiKey": API_KEY,
    "regions": "eu",
    "markets": "h2h,totals,btts",
    "oddsFormat": "decimal"
}

response = requests.get(url, params=params)

data = response.json()

os.makedirs("quotes", exist_ok=True)

with open("quotes/odds.json", "w") as f:
    json.dump(data, f, indent=4)

print("Quote aggiornate")
