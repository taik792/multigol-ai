import json

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

    o15 = o["over_1_5"]
    o25 = o["over_2_5"]

    # probabilità implicita
    p15 = 1 / o15
    p25 = 1 / o25

    # LOGICA REALE
    if p25 >= 0.60:
        pred = "Over 2.5"
        prob = round(p25 * 100)
        quota = o25
    elif p15 >= 0.75:
        pred = "Over 1.5"
        prob = round(p15 * 100)
        quota = o15
    else:
        continue

    predictions.append({
        "home": m["home"],
        "away": m["away"],
        "date": m["date"],
        "league": m["league"],
        "prediction": pred,
        "probability": prob,
        "odds": quota
    })

predictions = sorted(predictions, key=lambda x: -x["probability"])

output = {
    "top": predictions[:5],
    "all": predictions
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print("Predictions:", len(predictions))