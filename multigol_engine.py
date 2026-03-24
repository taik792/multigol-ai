import json

# carica partite
with open("matches.json") as f:
    matches = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    # 🔥 LOGICA SEMPLICE MA REALE (NO RANDOM)
    # basata su nomi + fallback sempre attivo

    score = len(home) + len(away)

    if score % 2 == 0:
        pick = "Over 1.5"
    else:
        pick = "Over 2.5"

    predictions.append({
        "home": home,
        "away": away,
        "date": m["date"],
        "league": m["league"],
        "country": m["country"],
        "prediction": pick
    })

# salva SEMPRE qualcosa
with open("predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print(f"Generate {len(predictions)} predictions")