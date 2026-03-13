import json
import math
import os
from datetime import datetime

def poisson(k, lam):
    return (lam ** k * math.exp(-lam)) / math.factorial(k)

# carica partite
with open("data/matches_today.json") as f:
    matches = json.load(f)

# carica statistiche squadre
with open("data/team_stats.json") as f:
    team_stats = json.load(f)

predictions = []

for match in matches:

    home_id = str(match["home_id"])
    away_id = str(match["away_id"])

    if home_id not in team_stats or away_id not in team_stats:
        continue

    home_stats = team_stats[home_id]
    away_stats = team_stats[away_id]

    home_attack = float(home_stats["goals_for"])
    home_def = float(home_stats["goals_against"])

    away_attack = float(away_stats["goals_for"])
    away_def = float(away_stats["goals_against"])

    # expected goals
    home_lambda = (home_attack + away_def) / 2
    away_lambda = (away_attack + home_def) / 2

    goal_probs = {}

    for h in range(6):
        for a in range(6):
            prob = poisson(h, home_lambda) * poisson(a, away_lambda)
            goal_probs[(h, a)] = prob

    over25 = 0
    btts = 0
    multigol_2_4 = 0

    home_goals = 0
    away_goals = 0

    for (h, a), p in goal_probs.items():

        total = h + a

        if total >= 3:
            over25 += p

        if h >= 1 and a >= 1:
            btts += p

        if 2 <= total <= 4:
            multigol_2_4 += p

        home_goals += h * p
        away_goals += a * p

    # multigol casa
    if home_goals < 1.2:
        home_range = "0-2"
    elif home_goals < 2:
        home_range = "1-3"
    else:
        home_range = "2-4"

    # multigol ospite
    if away_goals < 1.2:
        away_range = "0-2"
    elif away_goals < 2:
        away_range = "1-3"
    else:
        away_range = "2-4"

    # conversione data e ora
    match_time = datetime.fromisoformat(match["date"].replace("Z", "+00:00"))

    date_str = match_time.strftime("%d-%m-%Y")
    time_str = match_time.strftime("%H:%M")

    prediction = {
        "home": match["home"],
        "away": match["away"],
        "league": match["league"],
        "country": match["country"],
        "date": date_str,
        "time": time_str,
        "multigol": "2-4",
        "home_multigol": home_range,
        "away_multigol": away_range,
        "over25": round(over25 * 100, 1),
        "btts": round(btts * 100, 1),
        "probability": round(multigol_2_4 * 100, 1)
    }

    predictions.append(prediction)

print("Pronostici generati:", len(predictions))

os.makedirs("data", exist_ok=True)

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)