import json

# 📂 Carica partite
with open("data/matches_today.json", "r") as f:
    matches = json.load(f)

predictions = {
    "all": [],
    "top": []
}

for match in matches:
    try:
        fixture_id = match["fixture"]["id"]
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        # 🔥 previsione base (così non resta mai vuoto)
        plays = ["Over 1.5"]

        pred = {
            "fixture_id": fixture_id,
            "home": home,
            "away": away,
            "plays": plays
        }

        predictions["all"].append(pred)

    except Exception as e:
        print(f"Errore match saltato: {e}")
        continue

# 🔥 top picks = primi 5
predictions["top"] = predictions["all"][:5]

# 💾 salva file
with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print(f"✅ Generate {len(predictions['all'])} predictions")