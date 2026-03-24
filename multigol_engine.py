import json

with open("data/predictions.json", "w") as f:
    matches = json.load(f)

predictions = []

for m in matches:

    home = m.get("home", "Unknown")
    away = m.get("away", "Unknown")
    date = m.get("date", "")
    league = m.get("league", "Unknown")
    country = m.get("country", "Unknown")

    if "u19" in home.lower() or "u21" in home.lower():
        pick = "Over 2.5"
    else:
        pick = "Over 1.5"

    predictions.append({
        "home": home,
        "away": away,
        "date": date,
        "league": league,
        "country": country,
        "prediction": pick
    })

# 🔥 SALVA SOLO LISTA (IMPORTANTE)
with open("predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print(f"Generate {len(predictions)} predictions")