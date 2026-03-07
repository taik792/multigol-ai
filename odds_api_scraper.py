import json
import random

with open("data/matches_today.json") as f:
    matches = json.load(f)

odds = {}

for m in matches:

    home = m["home"]
    away = m["away"]

    key = f"{home} vs {away}"

    odds[key] = {
        "multigol_2_4": round(random.uniform(1.40, 2.10), 2)
    }

with open("quotes/odds.json", "w") as f:
    json.dump(odds, f, indent=4)

print("Odds generate:", len(odds))
