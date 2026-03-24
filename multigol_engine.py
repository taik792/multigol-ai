import json
import os

with open("data/matches.json") as f:
    matches = json.load(f)

with open("data/odds.json") as f:
    odds = json.load(f)

predictions = []

for m in matches:
    fid = str(m["fixture_id"])

    if fid not in odds:
        continue

    o = odds[fid]

    over15 = o.get("over_1_5", 0)
    over25 = o.get("over_2_5", 0)

    if over15 == 0:
        continue

    if over25 > 0 and over25 <= 1.80:
        prediction = "Over 2.5"
        quota = over25
    else:
        prediction = "Over 1.5"
        quota = over15

    probability = round(1 / quota, 2)

    predictions.append({
        "home": m["home"],
        "away": m["away"],
        "league": m.get("league", ""),
        "date": m["date"],
        "prediction": prediction,
        "odds": quota,
        "probability": probability
    })

predictions.sort(key=lambda x: x["probability"], reverse=True)

top = predictions[:10]

os.makedirs("data", exist_ok=True)

with open("data/predictions.json", "w") as f:
    json.dump({
        "top": top,
        "all": predictions
    }, f, indent=2)

print("Predictions:", len(predictions))