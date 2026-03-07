import json
import os

# carica partite
with open("data/matches_today.json") as f:
    matches = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    prediction = {
        "match": f"{home} vs {away}",
        "expected_goals": 2.8,
        "multigol": "2-4",
        "confidence": 75,
        "odds": {
            "over25": 1.70,
            "btts_yes": 1.65
        }
    }

    predictions.append(prediction)

# crea cartella output
os.makedirs("output", exist_ok=True)

# salva file finale
with open("output/multigol_predictions.json", "w") as f:
    json.dump(predictions, f, indent=4)

print("Multigol Engine completato")
