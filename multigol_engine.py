import json

# carica partite
with open("matches.json") as f:
    matches = json.load(f)

# carica quote
with open("odds.json") as f:
    odds_data = json.load(f)

predictions = []

for m in matches:

    fixture_id = m.get("fixture_id")

    odds = odds_data.get(str(fixture_id))

    if not odds:
        continue

    try:
        over15 = odds["over_1_5"]
        over25 = odds["over_2_5"]

        # converti quota → probabilità reale
        prob_over15 = 1 / over15
        prob_over25 = 1 / over25

        # scegli pick reale
        if prob_over25 > 0.55:
            pick = "Over 2.5"
            prob = round(prob_over25 * 100)
        elif prob_over15 > 0.65:
            pick = "Over 1.5"
            prob = round(prob_over15 * 100)
        else:
            continue  # scarta partite inutili

    except:
        continue

    predictions.append({
        "home": m.get("home"),
        "away": m.get("away"),
        "date": m.get("date"),
        "league": m.get("league"),
        "prediction": pick,
        "probability": prob
    })

# salva
with open("data/predictions.json", "w") as f:
    json.dump({
        "top": sorted(predictions, key=lambda x: -x["probability"])[:5],
        "all": predictions
    }, f, indent=2)

print("REAL PICKS:", len(predictions))