import json

# Carica matches
with open("data/matches.json") as f:
    matches = json.load(f)

# Carica odds
with open("data/odds.json") as f:
    odds_data = json.load(f)

predictions = []

for match in matches:
    fixture_id = str(match["fixture_id"])
    odds = odds_data.get(fixture_id)

    if not odds:
        continue

    over15 = odds.get("over_1_5")
    over25 = odds.get("over_2_5")

    prediction = None
    probability = 0
    selected_odds = 0

    # LOGICA REALE (basata su quote)
    if over25 and over25 >= 1.70:
        prediction = "Over 2.5"
        probability = int((1 / over25) * 100)
        selected_odds = over25
    elif over15 and over15 >= 1.20:
        prediction = "Over 1.5"
        probability = int((1 / over15) * 100)
        selected_odds = over15

    if prediction:
        predictions.append({
            "home": match["home"],
            "away": match["away"],
            "date": match["date"],
            "league": match.get("league", "N/A"),
            "prediction": prediction,
            "probability": probability,
            "odds": selected_odds
        })

# Top picks (filtra i migliori)
top = sorted(predictions, key=lambda x: x["probability"], reverse=True)[:5]

output = {
    "top": top,
    "all": predictions
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print("Predictions generate:", len(predictions))