import requests
import json
import os

API_KEY = os.getenv("37ddec86e8578a1ff3127d5c394da749")

headers = {
    "x-apisports-key": API_KEY
}

INPUT = "data/matches_today.json"
OUTPUT = "output/predictions.json"

if not os.path.exists(INPUT):

    with open(OUTPUT,"w") as f:
        json.dump([],f)

    exit()

with open(INPUT) as f:
    matches = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    # media gol globale reale calcio
    avg_goals = 2.6

    if avg_goals >= 2.5:
        over = "Over 2.5"
    else:
        over = "Under 2.5"

    if avg_goals >= 2.2:
        btts = "BTTS Yes"
    else:
        btts = "BTTS No"

    if avg_goals < 2.2:
        multigol = "1-2"
    elif avg_goals < 2.8:
        multigol = "2-3"
    else:
        multigol = "2-4"

    predictions.append({
        "home": home,
        "away": away,
        "over_under": over,
        "btts": btts,
        "multigol": multigol
    })

os.makedirs("output", exist_ok=True)

with open(OUTPUT,"w") as f:
    json.dump(predictions, f, indent=4)

print("Predictions:", len(predictions))
