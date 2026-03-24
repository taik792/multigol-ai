import json

with open("matches.json") as f:
    matches = json.load(f)

with open("odds.json") as f:
    odds_data = json.load(f)

predictions = []

for m in matches:

    fixture_id = str(m.get("fixture_id"))
    odds = odds_data.get(fixture_id)

    if not odds:
        continue

    try:
        over15 = float(odds["over_1_5"])
        over25 = float(odds["over_2_5"])

        prob_over15 = 1 / over15
        prob_over25 = 1 / over25

        pick = None
        prob = 0

        # 🎯 LOGICA SERIA
        if prob_over25 >= 0.60:
            pick = "Over 2.5"
            prob = round(prob_over25 * 100)
        elif prob_over15 >= 0.75:
            pick = "Over 1.5"
            prob = round(prob_over15 * 100)

        if not pick:
            continue

        predictions.append({
            "home": m.get("home"),
            "away": m.get("away"),
            "date": m.get("date"),
            "league": m.get("league"),
            "prediction": pick,
            "probability": prob,
            "odds": over25 if pick == "Over 2.5" else over15
        })

    except:
        continue

# 🔥 TOP PICKS = migliori probabilità
predictions = sorted(predictions, key=lambda x: -x["probability"])

output = {
    "top": predictions[:5],
    "all": predictions
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print("REAL PICKS:", len(predictions))