import json
import random

# ===== LOAD FILE =====
with open("data/matches_today.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

try:
    with open("data/quotes_manual.json", "r", encoding="utf-8") as f:
        manual_quotes = json.load(f)
except:
    manual_quotes = []

# ===== INDEX MANUAL BY FIXTURE =====
manual_map = {}
for q in manual_quotes:
    manual_map[q["fixture_id"]] = q

predictions = []

# ===== LOOP MATCHES =====
for match in matches:

    fixture_id = match.get("fixture_id")

    # =========================
    # 🔥 TOP PICK (MANUALE)
    # =========================
    if fixture_id in manual_map:
        q = manual_map[fixture_id]

        predictions.append({
            "home": match["home"],
            "away": match["away"],
            "league": match["league"],
            "date": match["date"],
            "time": match["time"],
            "pick": q["pick"],
            "prob": q["confidence"],
            "source": "quotes"
        })
        continue

    # =========================
    # 🤖 AI LOGICA REALE
    # =========================

    home_id = match.get("home_id", 0)
    away_id = match.get("away_id", 0)

    # pseudo strength (finché non mettiamo stats vere)
    home_strength = (home_id % 100) / 100
    away_strength = (away_id % 100) / 100

    diff = home_strength - away_strength

    if diff > 0.25:
        pick = "1"
        prob = 65 + int(diff * 100)
    elif diff < -0.25:
        pick = "2"
        prob = 65 + int(abs(diff) * 100)
    else:
        # equilibrio → goal
        if random.random() > 0.5:
            pick = "GG"
            prob = random.randint(55, 70)
        else:
            pick = "Over 2.5"
            prob = random.randint(55, 70)

    predictions.append({
        "home": match["home"],
        "away": match["away"],
        "league": match["league"],
        "date": match["date"],
        "time": match["time"],
        "pick": pick,
        "prob": prob,
        "source": "ai"
    })

# ===== SALVA =====
with open("data/predictions.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, indent=2, ensure_ascii=False)

print("Predictions generate:", len(predictions))