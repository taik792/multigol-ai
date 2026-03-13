import json

# carichiamo partite
with open("data/matches.json") as f:
    matches = json.load(f)

# carichiamo statistiche squadre
with open("data/team_stats.json") as f:
    stats = json.load(f)

predictions = []

for m in matches[:30]:

    home_id = str(m["home_id"])
    away_id = str(m["away_id"])

    if home_id not in stats or away_id not in stats:
        continue

    home_attack = stats[home_id]["scored"]
    home_defense = stats[home_id]["conceded"]

    away_attack = stats[away_id]["scored"]
    away_defense = stats[away_id]["conceded"]

    # goal attesi
    home_goals = (home_attack + away_defense) / 2
    away_goals = (away_attack + home_defense) / 2

    total_goals = home_goals + away_goals

    # OVER 2.5
    over25 = int(min(90, total_goals * 25))

    # BTTS
    btts = int(min(90, home_goals * away_goals * 30))

    # MULTIGOL TOTALE
    if total_goals < 2:
        multigol = "0-2"
    elif total_goals < 3:
        multigol = "1-3"
    elif total_goals < 4:
        multigol = "2-4"
    else:
        multigol = "3-5"

    # MULTIGOL CASA
    if home_goals < 1:
        home_multi = "0-1"
    elif home_goals < 2:
        home_multi = "1-2"
    else:
        home_multi = "2-3"

    # MULTIGOL OSPITE
    if away_goals < 1:
        away_multi = "0-1"
    elif away_goals < 2:
        away_multi = "1-2"
    else:
        away_multi = "2-3"

    probability = int(min(90, total_goals * 22))

    predictions.append({
        "home": m["home"],
        "away": m["away"],
        "league": m["league"],
        "multigol": multigol,
        "multigol_home": home_multi,
        "multigol_away": away_multi,
        "over25": over25,
        "btts": btts,
        "probability": probability
    })

# salviamo pronostici
with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print("Pronostici generati:", len(predictions))