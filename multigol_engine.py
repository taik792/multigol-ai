import json

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

    quote = odds.get(key, {})

    over15 = float(quote.get("over15",2.0))
    over25 = float(quote.get("over25",2.0))
    under25 = float(quote.get("under25",2.0))
    btts = float(quote.get("btts_yes",2.0))

    # stimiamo i gol attesi
    if over25 < 1.55:
        expected_goals = 3.2
    elif over25 < 1.75:
        expected_goals = 2.8
    elif over25 < 2.00:
        expected_goals = 2.4
    elif under25 < 1.70:
        expected_goals = 2.0
    else:
        expected_goals = 2.3

    # scelta multigol
    if expected_goals >= 3.1:

        multigol = "2-4"
        home_goals = "1-3"
        away_goals = "1-2"
        confidence = 86

    elif expected_goals >= 2.6:

        multigol = "2-3"
        home_goals = "1-2"
        away_goals = "1-2"
        confidence = 82

    elif expected_goals >= 2.2:

        multigol = "1-3"
        home_goals = "1-2"
        away_goals = "0-2"
        confidence = 79

    else:

        multigol = "0-2"
        home_goals = "0-1"
        away_goals = "0-1"
        confidence = 76

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
