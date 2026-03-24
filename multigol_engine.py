import json

# carica dati
with open("data/matches.json") as f:
    matches = json.load(f)

with open("odds.json") as f:
    odds_data = json.load(f)

predictions = []

for m in matches:

    fixture_id = str(m["fixture"]["id"])
    odds = odds_data.get(fixture_id)

    if not odds:
        continue

    o15 = odds.get("over_1_5")
    o25 = odds.get("over_2_5")

    if not o15 or not o25:
        continue

    # 🔥 LOGICA REALE (basata su quote)

    # Over 1.5 molto probabile
    if o15 <= 1.25:
        pred = "Over 1.5"
        prob = round((1 / o15) * 100)

    # Over 2.5 con valore
    elif 1.70 <= o25 <= 2.20:
        pred = "Over 2.5"
        prob = round((1 / o25) * 100)

    else:
        continue

    predictions.append({
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "date": m["fixture"]["date"],
        "league": m["league"]["name"],
        "prediction": pred,
        "probability": prob,
        "odds": o15 if pred == "Over 1.5" else o25
    })

# TOP PICKS (solo migliori)
top = sorted(predictions, key=lambda x: -x["probability"])[:10]

# salva
output = {
    "top": top,
    "all": predictions
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print("Predictions:", len(predictions))