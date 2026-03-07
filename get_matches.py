import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures?next=20"

headers = {
    "x-apisports-key": API_KEY,
    "x-apisports-host": "v3.football.api-sports.io"
}

# Richiesta API
response = requests.get(url, headers=headers)
data = response.json()

print("API RESPONSE:", data)

# Controllo se la risposta è corretta
if "response" not in data:
    print("Errore API o limite richieste")
    exit()

matches = []

for game in data["response"]:

    home = game["teams"]["home"]["name"]
    away = game["teams"]["away"]["name"]

    home_goals_avg = 1.5
    away_goals_avg = 1.2

    home_conceded = 1.2
    away_conceded = 1.4

    matches.append({
        "home": home,
        "away": away,
        "home_goals_avg": home_goals_avg,
        "away_goals_avg": away_goals_avg,
        "home_conceded": home_conceded,
        "away_conceded": away_conceded
    })

# Salva file per il motore multigol
with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Matches salvati in data/matches_today.json")
