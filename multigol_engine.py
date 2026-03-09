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

    home_id = match["home_id"]
    away_id = match["away_id"]
    league_id = match["league_id"]

    try:

        url_home = f"https://v3.football.api-sports.io/teams/statistics?league={league_id}&season=2024&team={home_id}"
        url_away = f"https://v3.football.api-sports.io/teams/statistics?league={league_id}&season=2024&team={away_id}"

        home_stats = requests.get(url_home, headers=headers).json()
        away_stats = requests.get(url_away, headers=headers).json()

        home_scored = float(home_stats["response"]["goals"]["for"]["average"]["home"])
        home_conceded = float(home_stats["response"]["goals"]["against"]["average"]["home"])

        away_scored = float(away_stats["response"]["goals"]["for"]["average"]["away"])
        away_conceded = float(away_stats["response"]["goals"]["against"]["average"]["away"])

    except:
        continue

    expected_home = (home_scored + away_conceded) / 2
    expected_away = (away_scored + home_conceded) / 2

    home_probs = [poisson(i, expected_home) for i in range(6)]
    away_probs = [poisson(i, expected_away) for i in range(6)]

    prob_btts = 1 - (home_probs[0] + away_probs[0] - (home_probs[0] * away_probs[0]))

    prob_over25 = 0

    for h in range(6):
        for a in range(6):

            if h + a >= 3:
                prob_over25 += home_probs[h] * away_probs[a]

    multigol_home = "1-3" if expected_home >= 1 else "0-2"
    multigol_away = "1-3" if expected_away >= 1 else "0-2"

    combo = "Casa" if expected_home > expected_away else "Ospite"

    probability = round(max(prob_over25, prob_btts) * 100)

    prediction = {
        "home": home,
        "away": away,
        "league": league,
        "time": time,
        "combo": combo,
        "multigol_home": multigol_home,
        "multigol_away": multigol_away,
        "over25": "Yes" if prob_over25 > 0.5 else "No",
        "btts": "Yes" if prob_btts > 0.5 else "No",
        "probability": probability
    }

    predictions.append(prediction)

with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, indent=4)

print("Predictions created:", len(predictions))