import json
import requests
import math

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

def poisson(k, lam):
    return (lam ** k * math.exp(-lam)) / math.factorial(k)

with open("matches.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

predictions = []

for match in matches:

    home = match["home"]
    away = match["away"]
    league = match["league"]
    time = match["time"]
    league_id = match["league_id"]
    home_id = match["home_id"]
    away_id = match["away_id"]

    # statistiche squadra casa
    url_home = f"https://v3.football.api-sports.io/teams/statistics?league={league_id}&season=2024&team={home_id}"
    home_stats = requests.get(url_home, headers=headers).json()

    # statistiche squadra ospite
    url_away = f"https://v3.football.api-sports.io/teams/statistics?league={league_id}&season=2024&team={away_id}"
    away_stats = requests.get(url_away, headers=headers).json()

    try:

        home_scored = home_stats["response"]["goals"]["for"]["average"]["home"]
        home_conceded = home_stats["response"]["goals"]["against"]["average"]["home"]

        away_scored = away_stats["response"]["goals"]["for"]["average"]["away"]
        away_conceded = away_stats["response"]["goals"]["against"]["average"]["away"]

        home_scored = float(home_scored)
        home_conceded = float(home_conceded)
        away_scored = float(away_scored)
        away_conceded = float(away_conceded)

    except:
        continue

    # expected goals
    expected_home = (home_scored + away_conceded) / 2
    expected_away = (away_scored + home_conceded) / 2

    # probabilità gol con Poisson
    home_probs = [poisson(i, expected_home) for i in range(5)]
    away_probs = [poisson(i, expected_away) for i in range(5)]

    # probabilità BTTS
    prob_btts = 1 - (home_probs[0] + away_probs[0] - (home_probs[0] * away_probs[0]))

    # probabilità over 2.5
    prob_over = 0
    for h in range(5):
        for a in range(5):
            if h + a >= 3:
                prob_over += home_probs[h] * away_probs[a]

    # multigol stimato
    multigol_home = "1-3" if expected_home >= 1 else "0-2"
    multigol_away = "1-3" if expected_away >= 1 else "0-2"

    prediction = {
        "home": home,
        "away": away,
        "league": league,
        "time": time,
        "multigol_home": multigol_home,
        "multigol_away": multigol_away,
        "over25": "Yes" if prob_over > 0.5 else "No",
        "btts": "Yes" if prob_btts > 0.5 else "No",
        "probability": round(max(prob_over, prob_btts) * 100)
    }

    predictions.append(prediction)

with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, indent=4)

print("Predictions created:", len(predictions