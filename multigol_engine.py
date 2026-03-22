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
# UTILS
# ===============================

def find_quote(fixture_id):
    for q in quotes:
        if q.get("fixture_id") == fixture_id:
            return q
    return None

def generate_pick(q):
    picks = []

    # 1X2
    if q["q1"] < 2:
        picks.append(("1", 60))
    if q["q2"] < 2:
        picks.append(("2", 60))
    if q["qx"] < 3:
        picks.append(("X", 55))

    # GG / NG
    if q["qgg"] < 1.80:
        picks.append(("GG", 65))
    if q["qng"] < 1.80:
        picks.append(("NG", 65))

    # OVER / UNDER
    if q["o_05"] < 1.50:
        picks.append(("Over 0.5", 75))
    if q["o_15"] < 2:
        picks.append(("Over 1.5", 70))
    if q["c_15"] < 2:
        picks.append(("Under 1.5", 65))

    # fallback
    if not picks:
        return "Over 1.5", 55

    pick = max(picks, key=lambda x: x[1])
    return pick

# ===============================
# MAIN ENGINE
# ===============================

predictions = []

for match in matches:
    fixture_id = match["fixture"]["id"]
    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]
    league = match["league"]["name"]
    date = match["fixture"]["date"]

    q = find_quote(fixture_id)

    if not q:
        continue

    pick, confidence = generate_pick(q)

    predictions.append({
        "fixture_id": fixture_id,
        "home": home,
        "away": away,
        "league": league,
        "date": date,
        "pick": pick,
        "confidence": confidence
    })

# ===============================
# TOP PICKS
# ===============================

top_picks = sorted(predictions, key=lambda x: x["confidence"], reverse=True)[:5]

# ===============================
# SAVE (FIX DEFINITIVO)
# ===============================

output = {
    "all": predictions,
    "top": top_picks
}

with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"✅ Generate {len(predictions)} predictions")