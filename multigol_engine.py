import json
import os

# carica partite
with open("data/matches_today.json", "r") as f:
    matches = json.load(f)

predictions = []

for m in matches:
    home = m.get("home")
    away = m.get("away")

    home_avg = float(m.get("home_goals_avg", 0))
    away_avg = float(m.get("away_goals_avg", 0))
    home_con = float(m.get("home_conceded", 0))
    away_con = float(m.get("away_conceded", 0))

    # stima gol attesi semplice
    xg = (home_avg + away_avg + home_con + away_con) / 2

    prediction = {
        "match": f"{home} vs {away}",
        "expected_goals": round(xg, 2),
        "multigol": "2-4",
        "confidence": int(min(max(xg * 30, 50), 95))
    }

    predictions.append(prediction)

# crea cartella output
os.makedirs("output", exist_ok=True)

# salva file
with open("output/multigol_predictions.json", "w") as f:
    json.dump(predictions, f, indent=4)

print("Multigol Engine completato")
print(predictions)
