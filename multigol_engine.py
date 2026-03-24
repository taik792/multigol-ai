import json

with open("data/matches_today.json", "r") as f:
    matches = json.load(f)

with open("data/team_stats.json", "r") as f:
    stats = json.load(f)

predictions = []

for m in matches:
    key_home = f"{m['home_id']}_{m['league_id']}"
    key_away = f"{m['away_id']}_{m['league_id']}"

    if key_home not in stats or key_away not in stats:
        continue

    home_stats = stats[key_home]
    away_stats = stats[key_away]

    home_attack = float(home_stats["goals_for"])
    away_attack = float(away_stats["goals_for"])

    home_def = float(home_stats["goals_against"])
    away_def = float(away_stats["goals_against"])

    # 🔥 modello base reale
    expected_goals = (home_attack + away_attack)

    if expected_goals >= 3:
        prediction = "Over 2.5"
    elif expected_goals >= 2:
        prediction = "Over 1.5"
    else:
        prediction = "Under 2.5"

    predictions.append({
        "home": m["home"],
        "away": m["away"],
        "date": m["date"],
        "league": m["league"],
        "country": m["country"],
        "prediction": prediction,
        "xg_estimate": round(expected_goals, 2)
    })

output = {
    "top": sorted(predictions, key=lambda x: x["xg_estimate"], reverse=True)[:5],
    "all": predictions
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Generate {len(predictions)} predictions REALI")