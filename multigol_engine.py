import json

# ===== LOAD =====
with open("data/matches_today.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

with open("data/quotes_manual.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

quotes_map = {q["fixture_id"]: q for q in quotes}

predictions = []

# ===== ENGINE =====
for match in matches:

    fixture_id = match.get("fixture_id")

    # SOLO partite con quote
    if fixture_id not in quotes_map:
        continue

    q = quotes_map[fixture_id]

    try:
        # probabilità implicite
        p1 = 1 / q["q1"]
        px = 1 / q["qx"]
        p2 = 1 / q["q2"]

        total = p1 + px + p2

        p1 /= total
        px /= total
        p2 /= total

        probs = {"1": p1, "X": px, "2": p2}

        pick = max(probs, key=probs.get)
        prob = round(probs[pick] * 100, 1)

        # filtro leggero (così non resta vuoto)
        if prob < 55:
            continue

    except:
        continue

    predictions.append({
        "home": match.get("home"),
        "away": match.get("away"),
        "prediction": pick,
        "probability": prob
    })

# ===== ORDINA =====
predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)

# ===== TOP PICKS =====
top_picks = predictions[:5]

# ===== SAVE =====
with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump({
        "all": predictions,
        "top": top_picks
    }, f, indent=2)

print(f"✅ Generate: {len(predictions)} picks")