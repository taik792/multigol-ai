import json
import random

with open("matches.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

predictions = []

for match in matches:

    home = match["home"]
    away = match["away"]
    league = match["league"]
    time = match["time"]

    multigol_home = random.choice(["1-2","1-3","2-3"])
    multigol_away = random.choice(["0-1","1-2","1-3"])

    # estrai valori minimi
    home_min = int(multigol_home.split("-")[0])
    away_min = int(multigol_away.split("-")[0])

    # BTTS logico
    if home_min >= 1 and away_min >= 1:
        btts = "Yes"
    else:
        btts = "No"

    # Over logico
    if home_min + away_min >= 3:
        over25 = "Yes"
    else:
        over25 = "No"

    probability = random.randint(60,85)

    combo = "Casa" if home_min > away_min else "Ospite"

    prediction = {
        "home": home,
        "away": away,
        "league": league,
        "time": time,
        "combo": combo,
        "multigol_home": multigol_home,
        "multigol_away": multigol_away,
        "over25": over25,
        "btts": btts,
        "probability": probability
    }

    predictions.append(prediction)

with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, indent=4)

print("Predictions created:", len(predictions))