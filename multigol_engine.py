import json
import os

# 📂 file
MATCHES_FILE = "matches.json"
QUOTES_FILE = "data/quotes_manual.json"
OUTPUT_FILE = "data/predictions.json"

def load_json(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

matches = load_json(MATCHES_FILE)
quotes = load_json(QUOTES_FILE)

predictions = []
top_picks = []

for match in matches:
    fid = match["fixture_id"]

    # trova quote
    q = next((x for x in quotes if x["fixture_id"] == fid), None)

    if not q:
        continue

    plays = []

    # 🔥 LOGICA REALE (semplice ma efficace)

    # GG
    if q.get("qgg", 0) <= 1.80:
        plays.append("GG")

    # NG
    if q.get("qng", 0) <= 1.80:
        plays.append("NG")

    # Over 1.5
    if q.get("c_o15", 0) <= 1.50:
        plays.append("Over 1.5")

    # Under 3.5
    if q.get("c_o35", 0) >= 1.40:
        plays.append("Under 3.5")

    # 1 fisso
    if q.get("q1", 10) <= 1.60:
        plays.append("1")

    # 2 fisso
    if q.get("q2", 10) <= 1.80:
        plays.append("2")

    if plays:
        pred = {
            "fixture_id": fid,
            "home": match["home"],
            "away": match["away"],
            "plays": plays
        }

        predictions.append(pred)

# 🔥 TOP PICK = primi 3 più sicuri
top_picks = predictions[:3]

# 🔥 salva SEMPRE qualcosa
output = {
    "all": predictions,
    "top": top_picks
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(output, f, indent=2)

print(f"✅ Predictions generate: {len(predictions)}")