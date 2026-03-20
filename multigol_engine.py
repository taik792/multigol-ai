import json
import os

with open("data/matches_today.json") as f:
    matches = json.load(f)

with open("data/team_stats.json") as f:
    team_stats = json.load(f)

predictions = []

for match in matches:

    home_id = str(match["home_id"])
    away_id = str(match["away_id"])

    if home_id not in team_stats or away_id not in team_stats:
        continue

    try:
        home_for = float(team_stats[home_id]["goals_for"])
        home_against = float(team_stats[home_id]["goals_against"])
        away_for = float(team_stats[away_id]["goals_for"])
        away_against = float(team_stats[away_id]["goals_against"])
    except:
        continue

    # 🔥 CALCOLO REALE
    expected_home = (home_for + away_against) / 2
    expected_away = (away_for + home_against) / 2

    total = expected_home + expected_away

    # 🎯 MULTIGOL
    if 2 <= total <= 4:
        multigol = "2-4"
    elif total < 2:
        multigol = "0-2"
    else:
        multigol = "3-5"

    casa = "1-3" if expected_home >= 1 else "0-2"
    ospite = "1-3" if expected_away >= 1 else "0-2"

    over25 = min((total / 4) * 100, 100)
    btts = min((expected_home * expected_away) / 4 * 100, 100)

    probability = (over25 + btts) / 2

    # 🔥 filtro qualità
    if probability < 45:
        continue

    predictions.append({
        "home": match["home"],
        "away": match["away"],
        "league": match["league"],
        "country": match["country"],
        "date": match["date"],
        "time": match["time"],
        "multigol": multigol,
        "home_multigol": casa,
        "away_multigol": ospite,
        "over25": round(over25, 1),
        "btts": round(btts, 1),
        "probability": round(probability, 1)
    })

# 🔥 TOP 10
predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)[:10]

print("Pronostici generati:", len(predictions))

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)