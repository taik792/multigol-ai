import json
import os

# carica partite
with open("data/matches_today.json") as f:
    matches = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    # simulazione statistica semplice
    over25 = 55
    btts = 48
    probability = 60

    pred = {
        "home": home,
        "away": away,
        "league": m.get("league", ""),
        "country": m.get("country", ""),
        "date": m.get("date", ""),

        "multigol": "2-4",
        "home_multigol": "1-3",
        "away_multigol": "1-2",

        "over25": over25,
        "btts": btts,
        "probability": probability
    }

    predictions.append(pred)

os.makedirs("data", exist_ok=True)

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print("Pronostici generati:", len(predictions))