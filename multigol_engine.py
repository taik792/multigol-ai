import json
import os

INPUT = "data/matches_today.json"
OUTPUT = "output/predictions.json"

if not os.path.exists(INPUT):
    print("No matches file")
    exit()

with open(INPUT) as f:
    matches = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    # stima base reale calcio
    expected_goals = 2.6

    if expected_goals < 2:
        multigol = "1-2"
    elif expected_goals < 3:
        multigol = "2-3"
    else:
        multigol = "2-4"

    over = "Over 2.5" if expected_goals >= 2.5 else "Under 2.5"

    btts = "Yes" if expected_goals >= 2.2 else "No"

    predictions.append({
        "home": home,
        "away": away,
        "multigol": multigol,
        "over_under": over,
        "btts": btts
    })

os.makedirs("output", exist_ok=True)

with open(OUTPUT,"w") as f:
    json.dump(predictions, f, indent=4)

print("Predictions created:", len(predictions))
