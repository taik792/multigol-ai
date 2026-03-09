import json

# carica le partite salvate
with open("matches.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

predictions = []

for match in matches:

    home = match["home"]
    away = match["away"]

    prediction = {
        "home": home,
        "away": away,
        "multigol": "2-3",
        "over25": "Yes",
        "btts": "Yes"
    }

    predictions.append(prediction)

# salva le previsioni
with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, indent=4, ensure_ascii=False)

print("Predictions created:", len(predictions))
