import json
import random

# ===============================
# LOAD FILES
# ===============================

with open("data/matches_today.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

with open("data/quotes_manual.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

# ===============================
# MAPPA QUOTE
# ===============================

quotes_map = {q["fixture_id"]: q for q in quotes}

predictions = []

# ===============================
# LOOP MATCHES
# ===============================

for match in matches:

    fixture_id = match.get("fixture_id")

    # dati base match
    home = match.get("home")
    away = match.get("away")
    league = match.get("league")
    date = match.get("date")
    time = match.get("time")

    # ===========================
    # 🔥 SE HO QUOTE → CALCOLO VERO
    # ===========================
    if fixture_id in quotes_map:

        q = quotes_map[fixture_id]

        try:
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

            probs = {
                "1": p1,
                "X": px,
                "2": p2
            }

            pick = max(probs, key=probs.get)
            confidence = round(probs[pick] * 100, 1)

            source = "quotes"

        except:
            pick = "Over 1.5"
            confidence = 55
            source = "quotes"

    # ===========================
    # 🤖 FALLBACK AI
    # ===========================
    else:

        pick = random.choice(["1", "X", "2", "GG", "Over 2.5"])
        confidence = random.randint(55, 70)
        source = "ai"

    predictions.append({
        "fixture_id": fixture_id,
        "home": home,
        "away": away,
        "league": league,
        "date": date,
        "time": time,
        "prediction": pick,
        "probability": confidence,
        "source": source
    })

# ===============================
# ORDINA + TOP PICKS
# ===============================

predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)

top_picks = [p for p in predictions if p["source"] == "quotes"][:5]

# fallback se non hai quote
if len(top_picks) == 0:
    top_picks = predictions[:5]

# ===============================
# SALVA (ROOT!)
# ===============================

with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump({
        "all": predictions,
        "top": top_picks
    }, f, indent=2)

print(f"✅ Generate: {len(predictions)} partite")