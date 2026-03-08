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
    away_win = float(quote.get("2",2.8))
    over25 = float(quote.get("over25",2.0))
    btts = float(quote.get("btts_yes",2.0))

    # stima gol totali
    if over25 < 1.55:
        total_goals = 3.3
    elif over25 < 1.75:
        total_goals = 2.8
    elif over25 < 1.95:
        total_goals = 2.5
    else:
        total_goals = 2.2

    # distribuzione casa / ospite
    if home_win < away_win:
        home_expected = total_goals * 0.6
        away_expected = total_goals * 0.4
    else:
        home_expected = total_goals * 0.4
        away_expected = total_goals * 0.6

    # scelta multigol
    if total_goals >= 3.1:
        multigol = random.choice(["2-4","2-5"])
    elif total_goals >= 2.6:
        multigol = random.choice(["2-3","1-4"])
    elif total_goals >= 2.3:
        multigol = random.choice(["1-3","1-2"])
    else:
        multigol = random.choice(["0-2","1-2"])

    # casa
    if home_expected > 1.7:
        home_goals = random.choice(["1-3","2-3"])
    elif home_expected > 1.2:
        home_goals = random.choice(["1-2","0-2"])
    else:
        home_goals = random.choice(["0-1","0-2"])

    # ospite
    if away_expected > 1.7:
        away_goals = random.choice(["1-3","2-3"])
    elif away_expected > 1.2:
        away_goals = random.choice(["1-2","0-2"])
    else:
        away_goals = random.choice(["0-1","0-2"])

    confidence = random.randint(75,90)

    predictions.append({
        "date": date,
        "home": home,
        "away": away,
        "multigol": multigol,
        "home_goals": home_goals,
        "away_goals": away_goals,
        "confidence": confidence
    })

# filtro confidence alta
predictions = [p for p in predictions if p["confidence"] >= 70]

# ordina per confidence
predictions = sorted(predictions,key=lambda x:x["confidence"],reverse=True)

# massimo 15 partite
predictions = predictions[:15]

with open("output/predictions.json","w") as f:
    json.dump(predictions,f,indent=4)

print("Top predictions:",len(predictions))

