import json

# ===== LOAD =====
with open("data/matches_today.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

with open("data/quotes_manual.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

quotes_map = {q["fixture_id"]: q for q in quotes}

predictions = []

# ===== ENGINE PRO =====
for match in matches:

    fixture_id = match.get("fixture_id")

    if fixture_id not in quotes_map:
        continue

    q = quotes_map[fixture_id]

    try:
        # ===== 1X2 =====
        p1 = 1 / q["q1"]
        px = 1 / q["qx"]
        p2 = 1 / q["q2"]

        total_1x2 = p1 + px + p2

        p1 /= total_1x2
        px /= total_1x2
        p2 /= total_1x2

        # ===== GG =====
        pgg = 1 / q["qgg"]
        png = 1 / q["qng"]

        total_gg = pgg + png

        pgg /= total_gg
        png /= total_gg

        # ===== OVER 2.5 =====
        pover = 1 / q["over25"]
        punder = 1 / q["under25"]

        total_ou = pover + punder

        pover /= total_ou
        punder /= total_ou

        # ===== MERCATI =====
        markets = {
            "1": p1,
            "X": px,
            "2": p2,
            "GG": pgg,
            "NG": png,
            "Over 2.5": pover,
            "Under 2.5": punder
        }

        pick = max(markets, key=markets.get)
        prob = round(markets[pick] * 100, 1)

        # ===== VALUE BET =====
        odds_map = {
            "1": q["q1"],
            "X": q["qx"],
            "2": q["q2"],
            "GG": q["qgg"],
            "NG": q["qng"],
            "Over 2.5": q["over25"],
            "Under 2.5": q["under25"]
        }

        value = markets[pick] * odds_map[pick]

        # ===== FILTRI PRO =====

        if prob < 60:
            continue

        if value < 1.05:
            continue

    except:
        continue

    predictions.append({
        "home": match.get("home"),
        "away": match.get("away"),
        "league": match.get("league"),
        "date": match.get("date"),
        "time": match.get("time"),
        "prediction": pick,
        "probability": prob,
        "value": round(value, 2)
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

print(f"🔥 PRO PICKS: {len(predictions)}")