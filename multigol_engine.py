import json
import random

with open("data/matches_today.json") as f:
    matches = json.load(f)

predictions = []

for m in matches:
    plays = []

    # logica base (poi miglioriamo)
    if random.random() > 0.5:
        plays.append("GG")
    else:
        plays.append("NG")

    if random.random() > 0.5:
        plays.append("Over 1.5")

    plays.append("1")

    predictions.append({
        "fixture_id": m["fixture_id"],
        "home": m["home"],
        "away": m["away"],
        "league": m.get("league", ""),
        "country": m.get("country", ""),
        "date": m.get("date", ""),
        "plays": plays
    })

# TOP PICKS (prime 2)
top = predictions[:2]

output = {
    "all": predictions,
    "top": top
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ Predictions generate")