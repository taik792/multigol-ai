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
    btts_yes = float(quote.get("btts_yes",2.0))
    btts_no = float(quote.get("btts_no",2.0))

    # partita molto aperta
    if over25 < 1.60 and btts_yes < 1.70:

        multigol = "2-4"
        home_goals = "1-3"
        away_goals = "1-2"
        confidence = 85

    # partita equilibrata
    elif over25 < 1.85:

        multigol = "2-3"
        home_goals = "1-2"
        away_goals = "1-2"
        confidence = 80

    # partita chiusa
    elif under25 < 1.70 or btts_no < 1.70:

        multigol = "0-2"
        home_goals = "0-1"
        away_goals = "0-1"
        confidence = 78

    else:

        multigol = "1-3"
        home_goals = "0-2"
        away_goals = "0-2"
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
