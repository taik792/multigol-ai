import json

# carica dati
with open("data/matches.json") as f:
    matches = json.load(f)

with open("odds.json") as f:
    odds_data = json.load(f)

predictions = []

# campionati seri
allowed_leagues = [
    "Premier League",
    "Serie A",
    "La Liga",
    "Bundesliga",
    "Ligue 1",
    "Championship",
    "Eredivisie"
]

for m in matches:

    fixture_id = str(m["fixture"]["id"])
    odds = odds_data.get(fixture_id)

    if not odds:
        continue

    o15 = odds.get("over_1_5")
    o25 = odds.get("over_2_5")

    if not o15 or not o25:
        continue

    league_name = m.get("league", {}).get("name", "N/A")

    # filtro campionati
    if league_name not in allowed_leagues:
        continue

    # 🔥 LOGICA REALE (ANTI FAKE)

    # scarta quote troppo basse
    if o15 <= 1.20:
        continue

    if o25 < 1.60:
        continue

    # scelta pronostico
    if 1.60 <= o25 <= 2.20:
        pred = "Over 2.5"
        prob = round((1 / o25) * 100)

    elif 1.25 <= o15 <= 1.45:
        pred = "Over 1.5"
        prob = round((1 / o15) * 100)

    else:
        continue

    predictions.append({
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "date": m["fixture"]["date"],
        "league": league_name,
        "prediction": pred,
        "probability": prob,
        "odds": o25 if pred == "Over 2.5" else o15
    })

# ordina migliori
predictions = sorted(predictions, key=lambda x: -x["probability"])

top = predictions[:10]

output = {
    "top": top,
    "all": predictions
}

# salva file GIUSTO (sito legge questo)
with open("data/predictions.json", "w") as f:
    json.dump(output, f, indent=2)

# salva anche debug
with open("predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print("Predictions generate:", len(predictions))