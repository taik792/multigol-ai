import json
import math

# carica partite
with open("data/matches.json") as f:
    matches = json.load(f)

# carica statistiche
with open("data/team_stats.json") as f:
    stats = json.load(f)

predictions = []

def poisson(avg, goals):
    return (avg ** goals * math.exp(-avg)) / math.factorial(goals)

for m in matches:

    home_id = str(m["home_id"])
    away_id = str(m["away_id"])

    if home_id not in stats or away_id not in stats:
        continue

    home = stats[home_id]
    away = stats[away_id]

    home_attack = home["scored"]
    home_defense = home["conceded"]

    away_attack = away["scored"]
    away_defense = away["conceded"]

    expected_home = (home_attack + away_defense) / 2
    expected_away = (away_attack + home_defense) / 2

    # calcolo over 2.5
    prob_under = 0
    for i in range(3):
        for j in range(3):
            if i + j <= 2:
                prob_under += poisson(expected_home, i) * poisson(expected_away, j)

    prob_over = 1 - prob_under

    # calcolo BTTS
    prob_home0 = poisson(expected_home, 0)
    prob_away0 = poisson(expected_away, 0)

    prob_btts = 1 - (prob_home0 + prob_away0 - (prob_home0 * prob_away0))

    # multigol range
    total_goals = expected_home + expected_away

    if total_goals <= 2:
        multigol = "0-2"
    elif total_goals <= 3:
        multigol = "1-3"
    elif total_goals <= 4:
        multigol = "2-4"
    else:
        multigol = "2-5"

    predictions.append({
        "home": m["home"],
        "away": m["away"],
        "league": m["league"],
        "over25": round(prob_over * 100),
        "btts": round(prob_btts * 100),
        "multigol": multigol
    })

# ordina per probabilità over
predictions = sorted(predictions, key=lambda x: x["over25"], reverse=True)

# prendi le migliori 30
predictions = predictions[:30]

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print("Pronostici generati:", len(predictions))