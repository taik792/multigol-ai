import json
import os

# carica partite
with open("data/matches_today.json") as f:
    matches = json.load(f)

# carica statistiche
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

    try:
        home_goals_for = float(home_stats["goals_for"])
        home_goals_against = float(home_stats["goals_against"])

        away_goals_for = float(away_stats["goals_for"])
        away_goals_against = float(away_stats["goals_against"])

    except:
        continue

    # ⚽ CALCOLO REALE
    expected_home = (home_goals_for + away_goals_against) / 2
    expected_away = (away_goals_for + home_goals_against) / 2

    total_goals = expected_home + expected_away

    # 🎯 MULTIGOL
    if 2 <= total_goals <= 4:
        multigol = "2-4"
    elif total_goals < 2:
        multigol = "0-2"
    else:
        multigol = "3-5"

    # 🏠 CASA
    if expected_home < 1:
        casa = "0-1"
    elif expected_home < 2:
        casa = "1-2"
    else:
        casa = "1-3"

    # ✈️ OSPITE
    if expected_away < 1:
        ospite = "0-1"
    elif expected_away < 2:
        ospite = "1-2"
    else:
        ospite = "1-3"

    # 📊 OVER / BTTS
    over25 = min((total_goals / 4) * 100, 100)
    btts = min(((expected_home * expected_away) / 4) * 100, 100)

    # 🧠 PROBABILITÀ FINALE
    probability = (over25 + btts) / 2

    # 🎯 FILTRO QUALITÀ
    if probability < 50:
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

# 🔥 ORDINA + LIMITA A 10
predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)
predictions = predictions[:10]

print("Pronostici generati:", len(predictions))

os.makedirs("data", exist_ok=True)

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)