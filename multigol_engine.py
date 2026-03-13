import json

with open("data/matches.json") as f:
    matches = json.load(f)

with open("data/team_stats.json") as f:
    stats = json.load(f)

predictions = []

for m in matches[:30]:

    home = str(m["home_id"])
    away = str(m["away_id"])

    if home not in stats or away not in stats:
        continue

    home_attack = stats[home]["scored"]
    home_defense = stats[home]["conceded"]

    away_attack = stats[away]["scored"]
    away_defense = stats[away]["conceded"]

    home_goals = (home_attack + away_defense) / 2
    away_goals = (away_attack + home_defense) / 2

    total_goals = home_goals + away_goals

    # Over 2.5
    over25 = min(90, int(total_goals * 25))

    # BTTS
    btts = min(90, int((home_goals * away_goals) * 30))

    # Multigol
    if total_goals < 2:
        multigol = "0-2"
    elif total_goals < 3:
        multigol = "1-3"
    elif total_goals < 4:
        multigol = "2-4"
    else:
        multigol = "3-5"

    probability = min(90, int(total_goals * 22))

    predictions.append({
        "home": m["home"],
        "away": m["away"],
        "league": m["league"],
        "multigol": multigol,
        "over25": over25,
        "btts": btts,
        "probability": probability
    })

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print("Pronostici generati:", len(predictions))