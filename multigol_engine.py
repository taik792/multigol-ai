import json

# carica partite
with open("data/matches_today.json", "r") as f:
    matches = json.load(f)

predictions = []

for m in matches:
    home = m["home"]
    away = m["away"]

    # 👉 REGOLA BASE (non random)
    prediction = "Over 1.5"

    # 👉 esempio filtro reale
    if "U18" in home or "U19" in home:
        prediction = "Over 2.5"

    if "Women" in home or "W" in home:
        prediction = "GG"

    predictions.append({
        "home": home,
        "away": away,
        "date": m["date"],
        "league": m["league"],
        "country": m["country"],
        "prediction": prediction
    })

# salva output
output = {
    "top": predictions[:5],
    "all": predictions
}

with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Generate {len(predictions)} predictions")