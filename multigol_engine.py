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

    # expected goals
    home_xg = (home_scored + away_conceded) / 2
    away_xg = (away_scored + home_conceded) / 2

    xg_total = home_xg + away_xg

    # probabilità
    probability = int((xg_total / 4) * 100)

    if probability < 50:
        probability = 50

    if probability > 85:
        probability = 85

    # over
    over25 = "Possibile" if xg_total > 2.4 else "Rischioso"

    # btts
    btts = "Possibile" if home_xg > 1 and away_xg > 1 else "Rischioso"

    # multigol casa
    if home_xg < 1:
        multigol_home = "0-2"
    elif home_xg < 2:
        multigol_home = "1-3"
    else:
        multigol_home = "2-4"

    # multigol ospite
    if away_xg < 1:
        multigol_away = "0-2"
    elif away_xg < 2:
        multigol_away = "1-3"
    else:
        multigol_away = "2-4"

    # combo
    if home_xg > away_xg:
        combo = "Casa o Over 1.5"
    elif away_xg > home_xg:
        combo = "Ospite o Over 1.5"
    else:
        combo = "Over 1.5"

    predictions.append({
        "home": home,
        "away": away,
        "league": m["league"],
        "time": m["time"],
        "combo": combo,
        "multigol_home": multigol_home,
        "multigol_away": multigol_away,
        "over25": over25,
        "btts": btts,
        "probability": probability
    })

# ordina per probabilità
predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)

# prende le 30 migliori
predictions = predictions[:30]

with open(OUTPUT_FILE, "w") as f:
    json.dump(predictions, f, indent=2)

print("Predictions generated:", len(predictions))