import json
import requests
import math

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

def poisson(k, lam):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

with open("matches.json", "r") as f:
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

    # media gol campionato standard
    league_avg_home = 1.35
    league_avg_away = 1.15

    # forza attacco
    attack_home = home_scored / league_avg_home
    attack_away = away_scored / league_avg_away

    # forza difesa
    defense_home = home_conceded / league_avg_away
    defense_away = away_conceded / league_avg_home

    # expected goals
    expected_home = attack_home * defense_away * league_avg_home
    expected_away = attack_away * defense_home * league_avg_away

    home_probs = [poisson(i, expected_home) for i in range(6)]
    away_probs = [poisson(i, expected_away) for i in range(6)]

    over25 = 0
    btts = 0

    for h in range(6):
        for a in range(6):

            p = home_probs[h] * away_probs[a]

            if h + a >= 3:
                over25 += p

            if h >= 1 and a >= 1:
                btts += p

    # multigol casa
    if expected_home < 0.8:
        multigol_home = "0-1"
    elif expected_home < 1.5:
        multigol_home = "0-2"
    else:
        multigol_home = "1-3"

    # multigol ospite
    if expected_away < 0.8:
        multigol_away = "0-1"
    elif expected_away < 1.5:
        multigol_away = "0-2"
    else:
        multigol_away = "1-3"

    # combo
    if expected_home > expected_away:
        combo = "Casa"
    elif expected_away > expected_home:
        combo = "Ospite"
    else:
        combo = "Pareggio"

    # probabilità corretta
    probability = int(max(over25, btts) * 100)

    if probability < 5:
        probability = 5

    predictions.append({

        "home": home,
        "away": away,
        "league": league,
        "time": time,
        "combo": combo,
        "multigol_home": multigol_home,
        "multigol_away": multigol_away,
        "over25": "Yes" if over25 > 0.5 else "No",
        "btts": "Yes" if btts > 0.5 else "No",
        "probability": probability

    })

with open("predictions.json", "w") as f:
    json.dump(predictions, f, indent=4)

print("Predictions created:", len(predictions))