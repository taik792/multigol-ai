import json
import random

# leggiamo le partite
with open("data/matches_today.json") as f:
    matches = json.load(f)

odds = {}

for match in matches:

    home = match["home"]
    away = match["away"]

    key = f"{home} vs {away}"

    odds[key] = {
        "multigol_2_4": round(random.uniform(1.40, 2.10), 2),
        "multigol_2_3": round(random.uniform(1.60, 2.20), 2)
    }

with open("quotes/odds.json", "w") as f:
    json.dump(odds, f, indent=4)

print("Odds create:", len(odds))
