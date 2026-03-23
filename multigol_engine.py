import json

def load(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return []

matches = load("data/matches_today.json")
quotes = load("data/quotes_manual.json")

predictions = []

for m in matches:
    fid = m["fixture_id"]
    q = next((x for x in quotes if x["fixture_id"] == fid), None)

    if not q:
        continue

    plays = []

    # 🔥 FILTRO QUALITÀ (NO partite strane)
    if q.get("q1", 10) < 1.20 or q.get("q2", 10) < 1.20:
        continue

    if q.get("q1", 10) > 5 and q.get("q2", 10) > 5:
        continue

    # 🔥 LOGICA PROFIT

    # GG forte
    if q.get("qgg", 10) <= 1.70:
        plays.append("GG")

    # NG forte
    elif q.get("qng", 10) <= 1.70:
        plays.append("NG")

    # Over sicuro
    if q.get("c_o15", 10) <= 1.40:
        plays.append("Over 1.5")

    # Under difensivo
    if q.get("c_o35", 10) >= 1.50:
        plays.append("Under 3.5")

    # Favorita forte
    if q.get("q1", 10) <= 1.55:
        plays.append("1")

    elif q.get("q2", 10) <= 1.80:
        plays.append("2")

    if len(plays) < 2:
        continue

    predictions.append({
        "fixture_id": fid,
        "home": m["home"],
        "away": m["away"],
        "plays": plays
    })

# 🔥 ORDINA (più affidabili prima)
predictions = predictions[:5]

top = predictions[:3]

output = {
    "all": predictions,
    "top": top
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"🔥 PROFIT PICKS: {len(predictions)}")