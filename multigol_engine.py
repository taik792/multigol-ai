import json
import os

# ===== LOAD MATCHES =====
if os.path.exists("data/matches.json"):
    with open("data/matches.json") as f:
        matches = json.load(f)
else:
    matches = []

# ===== LOAD ODDS =====
if os.path.exists("data/odds.json"):
    with open("data/odds.json") as f:
        odds = json.load(f)
else:
    odds = {}

predictions = []

print(f"Matches caricati: {len(matches)}")
print(f"Odds disponibili: {len(odds)}")

# ===== LOOP MATCHES =====
for m in matches:

    match_id = str(m.get("fixture_id"))  # 🔥 FIX IMPORTANTE

    o = odds.get(match_id)

    if not o:
        continue

    over15 = o.get("over_1_5")
    over25 = o.get("over_2_5")

    if not over15 or not over25:
        continue

    # ===== LOGICA REALE (basata su quote) =====
    if over25 <= 1.80:
        prediction = "Over 2.5"
        prob = round((1 / over25) * 100)
        odd = over25
    else:
        prediction = "Over 1.5"
        prob = round((1 / over15) * 100)
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

# ===== TOP PICKS =====
top = sorted(predictions, key=lambda x: x["probability"], reverse=True)[:5]

# ===== OUTPUT =====
output = {
    "top": top,
    "all": predictions
}

# crea cartella se manca
os.makedirs("data", exist_ok=True)

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Predictions generate: {len(predictions)}")
print("✅ ENGINE OK")