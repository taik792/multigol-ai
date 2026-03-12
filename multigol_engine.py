import json

with open("matches.json") as f:
    matches = json.load(f)

with open("teams_stats.json") as f:
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

    total = expected_home + expected_away

    over25 = int(min(100, total * 30))
    btts = int(min(100, (expected_home * expected_away) * 25))

    probability = int((over25 + btts) / 2)

    predictions.append({
        "home": home,
        "away": away,
        "league": m["league"],
        "country": m["country"],
        "time": m["time"],
        "over25": over25,
        "btts": btts,
        "probability": probability
    })

predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)

predictions = predictions[:30]

with open("predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print("Pronostici generati:", len(predictions))