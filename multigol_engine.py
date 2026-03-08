import json
import os

INPUT = "quotes/odds_today.json"
OUTPUT = "output/predictions.json"

if not os.path.exists(INPUT):

    with open(OUTPUT,"w") as f:
        json.dump([],f)

    exit()

with open(INPUT) as f:
    matches = json.load(f)

predictions = []

for m in matches:

    o25 = m["over25"]
    o35 = m["over35"]

    p25 = 1 / o25
    p35 = 1 / o35

    diff = p25 - p35

    if diff > 0.18:
        mg = "1-3"
    elif diff > 0.12:
        mg = "2-4"
    elif diff > 0.07:
        mg = "2-5"
    else:
        mg = "3-6"

    predictions.append({
        "home": m["home"],
        "away": m["away"],
        "multigol": mg
    })

os.makedirs("output", exist_ok=True)

with open(OUTPUT,"w") as f:
    json.dump(predictions[:10],f,indent=4)

print("Pronostici creati:",len(predictions))
