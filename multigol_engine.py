import json

with open("data/matches_today.json") as f:
    matches = json.load(f)

with open("quotes/odds.json") as f:
    odds = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    match_key = f"{home} vs {away}"

    quote = odds.get(match_key, {}).get("multigol_2_4", None)

    if quote:
        if quote < 1.50:
            multigol = "2-4"
            confidence = 85
        elif quote < 1.80:
            multigol = "2-3"
            confidence = 80
        else:
            multigol = "1-3"
            confidence = 75
    else:
        multigol = "1-3"
        confidence = 70

    predictions.append({
        "home": home,
        "away": away,
        "multigol": multigol,
        "home_goals": "1-3",
        "away_goals": "0-2",
        "confidence": confidence,
        "quota": quote
    })

with open("output/predictions.json", "w") as f:
    json.dump(predictions, f, indent=4)

print("Pronostici creati:", len(predictions))
