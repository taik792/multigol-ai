import json

with open("matches_today.json") as f:
matches = json.load(f)

predictions = []

for m in matches:

home = m["home"]
away = m["away"]

home_power = len(home) % 5 + 1
away_power = len(away) % 5 + 1

total = home_power + away_power

if total >= 6:
    over = "Yes"
else:
    over = "No"

if home_power > 2 and away_power > 2:
    btts = "Yes"
else:
    btts = "No"

probability = int((total / 10) * 100)

if probability < 40:
    continue

prediction = {
    "home": home,
    "away": away,
    "league": m["league"],
    "time": m["time"],
    "combo": "Casa" if home_power > away_power else "Ospite",
    "multigol_home": "1-3",
    "multigol_away": "1-3",
    "over25": over,
    "btts": btts,
    "probability": probability
}

predictions.append(prediction)

predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)

predictions = predictions[:30]

with open("predictions.json", "w") as f:
json.dump(predictions, f, indent=4)

print("Partite selezionate:", len(predictions))