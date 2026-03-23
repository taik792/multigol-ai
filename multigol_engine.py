import json
import random

with open("data/matches_today.json") as f:
    matches = json.load(f)

predictions = []
top_picks = []

for match in matches:

    prob = random.randint(55, 75)

    plays = []

    if prob > 60:
        plays.append("Over 1.5")

    if prob > 65:
        plays.append("GG")

    if prob > 58:
        plays.append("1")

    pred = {
        "home": match["home"],
        "away": match["away"],
        "league": match["league"],
        "country": match["country"],
        "date": match["date"],
        "plays": plays,
        "probability": prob
    }

    predictions.append(pred)

    if prob >= 65:
        top_picks.append(pred)

output = {
    "all": predictions,
    "top": top_picks
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=4)

print("🔥 Predictions generate")