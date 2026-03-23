import json

with open("data/matches_today.json") as f:
    matches = json.load(f)

with open("data/team_stats.json") as f:
    stats = json.load(f)

predictions = []

for m in matches:
    home = m["home"]
    away = m["away"]

    home_scored = stats.get(home, {}).get("scored", 1.2)
    home_conceded = stats.get(home, {}).get("conceded", 1.2)

    away_scored = stats.get(away, {}).get("scored", 1.2)
    away_conceded = stats.get(away, {}).get("conceded", 1.2)

    # ⚽ forza offensiva
    home_attack = (home_scored + away_conceded) / 2
    away_attack = (away_scored + home_conceded) / 2

    total_goals = home_attack + away_attack

    plays = []

    # 🎯 LOGICA REALE
    if total_goals >= 2.5:
        plays.append("Over 2.5")
    elif total_goals >= 2:
        plays.append("Over 1.5")

    if home_attack > away_attack * 1.2:
        plays.append("1")
    elif away_attack > home_attack * 1.2:
        plays.append("2")

    if home_attack > 1 and away_attack > 1:
        plays.append("GG")

    if not plays:
        continue

    predictions.append({
        "home": home,
        "away": away,
        "date": m["date"],
        "league": m["league"],
        "country": m["country"],
        "plays": plays,
        "strength": total_goals
    })

# 🔥 TOP PICKS = migliori per goal attesi
predictions = sorted(predictions, key=lambda x: x["strength"], reverse=True)

output = {
    "top": predictions[:5],
    "all": predictions
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Generate {len(predictions)} predictions")