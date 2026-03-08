import json
import random

# carica partite trovate
with open("data/matches_today.json") as f:
    matches = json.load(f)

# carica quote
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
        confidence = random.randint(80,90)

    elif over25 < 1.80:
        multigol = "2-3"
        confidence = random.randint(75,85)

    else:
        multigol = "1-3"
        confidence = random.randint(70,80)

    predictions.append({
        "home": home,
        "away": away,
        "multigol": multigol,
        "confidence": confidence
    })

# SALVA NEL FILE CHE IL SITO LEGGE
with open("output/predictions.json","w") as f:
    json.dump(predictions,f,indent=4)

print("Predictions generate:",len(predictions))
