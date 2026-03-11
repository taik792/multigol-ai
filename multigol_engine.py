import json

with open("data/matches_today.json") as f:
    matches = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]
    league = m["league"]
    time = m["time"]

    prediction = {
        "home": home,
        "away": away,
        "league": league,
        "time": time,
        "combo": "Da analizzare",
        "multigol_home": "0-2",
        "multigol_away": "0-2",
        "over25": "Da calcolare",
        "btts": "Da calcolare",
        "probability": 50
    }

    predictions.append(prediction)

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=4)
