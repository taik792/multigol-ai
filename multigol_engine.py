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

    # stima semplice basata su media gol tipica
    # (senza dati inventati)

    avg_goals = 2.6

    if avg_goals < 2.3:
        mg = "1-2"
    elif avg_goals < 2.8:
        mg = "2-3"
    else:
        mg = "2-4"

    predictions.append({
        "home": home,
        "away": away,
        "multigol": mg
    })

os.makedirs("output", exist_ok=True)

with open(OUTPUT,"w") as f:
    json.dump(predictions[:10],f,indent=4)

print("Pronostici creati:",len(predictions))
