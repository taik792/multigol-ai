import json

with open("data/matches_today.json") as f:
    matches = json.load(f)

with open("quotes/odds.json") as f:
    odds = json.load(f)

predictions = []

for match in matches:

    home = match["home"]
    away = match["away"]

    key = f"{home}-{away}"

    quote = odds.get(key)

    if not quote:
        continue

    over25 = quote["over25"]

    if over25 < 1.60:
        multigol = "2-4"
        confidence = 85

    elif over25 < 1.80:
        multigol = "2-3"
        confidence = 80

    else:
        multigol = "1-3"
        confidence = 75

    predictions.append({
        "home": home,
        "away": away,
        "multigol": multigol,
        "confidence": confidence
    })

with open("output/predictions.json","w") as f:
    json.dump(predictions,f,indent=4)

print("Pronostici generati:",len(predictions))
