import json
import random

with open("data/matches_today.json") as f:
    matches = json.load(f)

with open("quotes/odds.json") as f:
    odds = json.load(f)

predictions = []

for match in matches:

    home = match["home"]
    away = match["away"]

    key = f"{home}-{away}"

    quote_data = odds.get(key, {})

    over25 = quote_data.get("over25", 2.0)

    if over25 < 1.60:
        multigol = "2-4"
        home_goals = "1-3"
        away_goals = "1-2"
        confidence = random.randint(80,90)

    elif over25 < 1.80:
        multigol = "2-3"
        home_goals = "1-2"
        away_goals = "1-2"
        confidence = random.randint(75,85)

    else:
        multigol = "1-3"
        home_goals = "0-2"
        away_goals = "0-2"
        confidence = random.randint(70,80)

    predictions.append({
        "home": home,
        "away": away,
        "multigol": multigol,
        "home_goals": home_goals,
        "away_goals": away_goals,
        "confidence": confidence
    })

with open("output/predictions.json","w") as f:
    json.dump(predictions,f,indent=4)

print("Predictions generate:",len(predictions))
