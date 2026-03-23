import json
import random

# carica partite
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

    # 🔥 FIX IMPORTANTE → campi sempre presenti
    pred = {
        "home": match.get("home", ""),
        "away": match.get("away", ""),
        "league": match.get("league", "Unknown"),
        "country": match.get("country", "Unknown"),
        "date": match.get("date", ""),
        "plays": plays if plays else ["No bet"],
        "probability": prob
    }

    predictions.append(pred)

    if prob >= 65:
        top_picks.append(pred)

output = {
    "all": predictions,
    "top": top_picks if top_picks else predictions[:2]  # fallback
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=4)

print("🔥 Predictions generate OK")