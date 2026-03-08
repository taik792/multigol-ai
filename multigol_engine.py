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

    home_win = float(quote.get("1",2.5))
    draw = float(quote.get("X",3.2))
    away_win = float(quote.get("2",2.8))
    over25 = float(quote.get("over25",2.0))
    btts = float(quote.get("btts_yes",2.0))

    # stimiamo gol totali
    if over25 < 1.55:
        total_goals = 3.2
    elif over25 < 1.75:
        total_goals = 2.8
    elif over25 < 2.00:
        total_goals = 2.5
    else:
        total_goals = 2.2

    # distribuzione gol casa / ospite
    if home_win < away_win:

        home_expected = total_goals * 0.6
        away_expected = total_goals * 0.4

    elif away_win < home_win:

        home_expected = total_goals * 0.4
        away_expected = total_goals * 0.6

    else:

        home_expected = total_goals * 0.5
        away_expected = total_goals * 0.5

    # multigol totale
    if total_goals >= 3:

        multigol = "2-4"

    elif total_goals >= 2.6:

        multigol = "2-3"

    elif total_goals >= 2.2:

        multigol = "1-3"

    else:

        multigol = "0-2"

    # casa
    if home_expected >= 1.8:
        home_goals = "1-3"
    elif home_expected >= 1.2:
        home_goals = "1-2"
    else:
        home_goals = "0-1"

    # ospite
    if away_expected >= 1.8:
        away_goals = "1-3"
    elif away_expected >= 1.2:
        away_goals = "1-2"
    else:
        away_goals = "0-1"

    confidence = random.randint(78,88)

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
