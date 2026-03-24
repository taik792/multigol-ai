import json

# carica matches
with open("data/matches.json") as f:
    matches = json.load(f)

# carica odds
with open("data/odds.json") as f:
    odds = json.load(f)

predictions = []

for match in matches:
    fixture_id = str(match["fixture_id"])

    if fixture_id not in odds:
        continue

    o = odds[fixture_id]

    if o["over_2_5"] >= 1.80:
        pred = "Over 2.5"
        prob = 75
        quota = o["over_2_5"]
    else:
        pred = "Over 1.5"
        prob = 85
        quota = o["over_1_5"]

    predictions.append({
        "home": match["home"],
        "away": match["away"],
        "date": match["date"],
        "league": match.get("league", ""),
        "prediction": pred,
        "probability": prob,
        "odds": quota
    })

output = {
    "top": predictions[:10],
    "all": predictions
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print("Predictions generate:", len(predictions))