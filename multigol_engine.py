import json

# carica matches
with open("data/matches.json") as f:
    matches = json.load(f)

# carica odds
with open("data/odds.json") as f:
    odds = json.load(f)

predictions = []

for m in matches:
    match_id = str(m.get("id"))

    # prendi odds reali
    o = odds.get(match_id)

    if not o:
        continue

    over15 = o.get("over_1_5")
    over25 = o.get("over_2_5")

    if not over15 or not over25:
        continue

    # logica reale basata su quota
    if over25 <= 1.80:
        prediction = "Over 2.5"
        prob = int((1 / over25) * 100)
        odd = over25
    else:
        prediction = "Over 1.5"
        prob = int((1 / over15) * 100)
        odd = over15

    predictions.append({
        "home": m.get("home"),
        "away": m.get("away"),
        "date": m.get("date"),
        "league": m.get("league", "Unknown"),
        "prediction": prediction,
        "probability": prob,
        "odds": odd
    })

# TOP picks veri (quota bassa + alta probabilità)
top = sorted(predictions, key=lambda x: x["probability"], reverse=True)[:5]

# salva
output = {
    "top": top,
    "all": predictions
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ Predictions generate REALI")