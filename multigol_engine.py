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

    probability = random.randint(60,85)

    combo = random.choice(["Casa","Ospite"])

    prediction = {
        "home": home,
        "away": away,
        "league": league,
        "time": time,
        "combo": combo,
        "multigol_home": multigol_home,
        "multigol_away": multigol_away,
        "over25": random.choice(["Yes","No"]),
        "btts": random.choice(["Yes","No"]),
        "probability": probability
    }

    predictions.append(prediction)

with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, indent=4)

print("Predictions created:", len(predictions))
