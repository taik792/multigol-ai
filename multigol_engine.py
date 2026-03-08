import json
import os

INPUT_FILE = "quotes/odds_today.json"
OUTPUT_FILE = "output/predictions.json"

def calculate_multigol(odds):

    o25 = odds.get("over_2_5")
    o35 = odds.get("over_3_5")

    if not o25 or not o35:
        return None

    p25 = 1 / o25
    p35 = 1 / o35

    diff = p25 - p35

    if diff > 0.18:
        return "1-3"

    if diff > 0.12:
        return "2-4"

    if diff > 0.07:
        return "2-5"

    return "3-6"


if not os.path.exists(INPUT_FILE):

    with open(OUTPUT_FILE, "w") as f:
        json.dump([], f)

    exit()

with open(INPUT_FILE) as f:
    matches = json.load(f)

predictions = []

for match in matches:

    home = match["home"]
    away = match["away"]
    odds = match["odds"]

    multigol = calculate_multigol(odds)

    if multigol is None:
        continue

    predictions.append({
        "home": home,
        "away": away,
        "multigol": multigol
    })

predictions = predictions[:10]

os.makedirs("output", exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    json.dump(predictions, f, indent=4)

print("Pronostici generati:", len(predictions))