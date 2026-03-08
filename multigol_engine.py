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
    date = match.get("date","")

    key = f"{home}-{away}"

    quote = odds.get(key,{})

    over15 = float(quote.get("over15",2.0))
    over25 = float(quote.get("over25",2.0))
    under25 = float(quote.get("under25",2.0))
    btts = float(quote.get("btts_yes",2.0))

    # stima gol
    goal_score = 0

    if over15 < 1.35:
        goal_score += 1

    if over25 < 1.70:
        goal_score += 1

    if btts < 1.75:
        goal_score += 1

    if under25 < 1.65:
        goal_score -= 1

    # scelta multigol
    if goal_score >= 2:

        multigol = "2-4"
        home_goals = random.choice(["1-2","1-3","2-3"])
        away_goals = random.choice(["1-2","0-2"])
        confidence = 85

    elif goal_score == 1:

        multigol = "2-3"
        home_goals = random.choice(["1-2","1-3"])
        away_goals = random.choice(["1-2"])
        confidence = 82

    elif goal_score == 0:

        multigol = "1-3"
        home_goals = random.choice(["0-2","1-2"])
        away_goals = random.choice(["0-2","1-2"])
        confidence = 78

    else:

        multigol = "0-2"
        home_goals = random.choice(["0-1"])
        away_goals = random.choice(["0-1"])
        confidence = 75

    predictions.append({
        "date": date,
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
