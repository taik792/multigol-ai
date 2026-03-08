import json
import random

with open("data/matches_today.json") as f:
    matches = json.load(f)

with open("quotes/odds.json") as f:
    odds = json.load(f)

predictions = []

for match in matches:

    key = match["home"] + " vs " + match["away"]

    if key not in odds:
        continue

    over15 = odds[key].get("Over 1.5", 2)
    over25 = odds[key].get("Over 2.5", 2)
    under25 = odds[key].get("Under 2.5", 2)

    expected_goals = 2.5

    if over25 < 1.80:
        multigol = "2-4"
        expected_goals = 3
    elif under25 < 1.80:
        multigol = "0-2"
        expected_goals = 1.8
    else:
        multigol = "1-3"

    home_goals = random.choice(["0-1", "0-2", "1-2"])
    away_goals = random.choice(["0-1", "0-2", "1-2"])

    confidence = random.randint(70, 85)

    predictions.append({
        "date": match["date"],
        "match": key,
        "league": match["league"],
        "multigol": multigol,
        "home_range": home_goals,
        "away_range": away_goals,
        "confidence": confidence
    })

predictions = sorted(predictions, key=lambda x: x["confidence"], reverse=True)[:10]

with open("output/multigol_predictions.json", "w") as f:
    json.dump(predictions, f, indent=4)

print("Predizioni generate:", len(predictions))
