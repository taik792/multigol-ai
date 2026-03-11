import json

MATCHES_FILE = "data/matches_today.json"
STATS_FILE = "data/teams_stats.json"
OUTPUT_FILE = "data/predictions.json"

with open(MATCHES_FILE) as f:
    matches = json.load(f)

with open(STATS_FILE) as f:
    stats = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    if home not in stats or away not in stats:
        continue

    home_scored = stats[home]["scored"]
    home_conceded = stats[home]["conceded"]

    away_scored = stats[away]["scored"]
    away_conceded = stats[away]["conceded"]

    expected_home = (home_scored + away_conceded) / 2
    expected_away = (away_scored + home_conceded) / 2

    total_goals = expected_home + expected_away

    probability = int(total_goals * 25)

    if probability > 90:
        probability = 90

    predictions.append({
        "home": home,
        "away": away,
        "league": m["league"],
        "time": m["time"],
        "combo": "Casa o Over 1.5",
        "multigol_home": "1-3",
        "multigol_away": "0-2",
        "over25": "Possibile",
        "btts": "Possibile",
        "probability": probability
    })

# prende le 30 migliori
predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)[:30]

with open(OUTPUT_FILE, "w") as f:
    json.dump(predictions, f, indent=2)

print("Predictions generated:", len(predictions))