import json
import random

# Carica matches
with open("data/matches_today.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

# Carica quote manuali
with open("data/quotes_manual.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

# Mappa per fixture_id
quotes_map = {q["fixture_id"]: q for q in quotes}

predictions = []

for match in matches:

    fixture_id = match.get("fixture_id")

    if fixture_id not in quotes_map:
        continue

    q = quotes_map[fixture_id]

    # LOGICA BASE (tipo Colab)
    q1 = q["q1"]
    qx = q["qx"]
    q2 = q["q2"]

    # probabilità inverse
    p1 = 1 / q1
    px = 1 / qx
    p2 = 1 / q2

    total = p1 + px + p2

    p1 /= total
    px /= total
    p2 /= total

    # pick migliore
    probs = {
        "1": p1,
        "X": px,
        "2": p2
    }

    pick = max(probs, key=probs.get)
    confidence = round(probs[pick] * 100, 1)

    predictions.append({
        "fixture_id": fixture_id,
        "home": match["home"],
        "away": match["away"],
        "league": match.get("league", ""),
        "date": match.get("date", ""),
        "time": match.get("time", ""),
        "prediction": pick,
        "probability": confidence
    })

# Ordina per probabilità
predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)

# TOP PICK (prime 10)
top_picks = predictions[:10]

# Salva output
with open("data/predictions.json", "w", encoding="utf-8") as f:
    json.dump({
        "all": predictions,
        "top": top_picks
    }, f, indent=2)

print(f"Predictions generate: {len(predictions)}")
print(f"Top picks: {len(top_picks)}")