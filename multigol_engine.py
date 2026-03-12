import json

with open("matches.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

with open("teams_stats.json", "r", encoding="utf-8") as f:
    stats = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    home_scored = stats.get(home, {}).get("scored", 1.2)
    home_conceded = stats.get(home, {}).get("conceded", 1.2)

    away_scored = stats.get(away, {}).get("scored", 1.2)
    away_conceded = stats.get(away, {}).get("conceded", 1.2)

    # gol attesi
    home_goal_expect = (home_scored + away_conceded) / 2
    away_goal_expect = (away_scored + home_conceded) / 2

    total_goals = home_goal_expect + away_goal_expect

    over25 = min(95, int(total_goals * 35))
    btts = min(90, int((home_goal_expect * away_goal_expect) * 30))

    probability = int((over25 * 0.6) + (btts * 0.4))

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

with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, indent=2)

print("Pronostici generati:", len(predictions))