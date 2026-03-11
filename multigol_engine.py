import json
import os

# carica partite
with open("data/matches_today.json") as f:
    matches = json.load(f)

# carica statistiche squadre
with open("data/teams_stats.json") as f:
    stats = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    home_stats = stats.get(home)
    away_stats = stats.get(away)

    if not home_stats or not away_stats:
        continue

    home_scored = home_stats["scored"]
    away_scored = away_stats["scored"]

    home_conceded = home_stats["conceded"]
    away_conceded = away_stats["conceded"]

    expected_home = (home_scored + away_conceded) / 2
    expected_away = (away_scored + home_conceded) / 2

    expected_goals = expected_home + expected_away

    probability = round(min(90, expected_goals * 25))

    prediction = {

        "home": home,
        "away": away,

        "league": m["league"],
        "country": m.get("country",""),

        "time": m["time"],

        "combo": "Casa o Over 1.5",

        "multigol_home": "1-3",
        "multigol_away": "1-3",

        "over25": "Possibile",
        "btts": "Possibile",

        "probability": probability
    }

    predictions.append(prediction)

os.makedirs("data", exist_ok=True)

with open("data/predictions.json","w") as f:
    json.dump(predictions,f,indent=2)

print("Predictions generate:",len(predictions))