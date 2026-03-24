import json

# carica matches
with open("matches.json") as f:
    matches = json.load(f)

predictions = []

for m in matches:

    # ✅ safe read (qualsiasi formato)
    home = m.get("home", "")
    away = m.get("away", "")
    date = m.get("date", "")

    # FIX league (supporta più formati)
    if isinstance(m.get("league"), dict):
        league = m["league"].get("name", "Unknown")
    else:
        league = m.get("league", "Unknown")

    country = m.get("country", "Unknown")

    # 🧠 LOGICA BASE (non random)
    if "u19" in home.lower() or "u21" in home.lower():
        prediction = "Over 2.5"
        prob = 65
    else:
        prediction = "Over 1.5"
        prob = 60

    predictions.append({
        "home": home,
        "away": away,
        "date": date,
        "league": league,
        "country": country,
        "prediction": prediction,
        "probability": prob
    })

# salva dove legge il sito
with open("data/predictions.json", "w") as f:
    json.dump({
        "top": predictions[:5],
        "all": predictions
    }, f, indent=2)

print("OK predictions:", len(predictions))