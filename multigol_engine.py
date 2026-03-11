import json

with open("data/matches_today.json") as f:
    matches = json.load(f)

predictions = []

top_leagues = [
"Serie A",
"Premier League",
"La Liga",
"Bundesliga",
"Ligue 1",
"Championship",
"Primeira Liga",
"Eredivisie",
"MLS",
"Brasileiro Serie A"
]

for m in matches:

    league = m["league"]

    if league not in top_leagues:
        continue

    home = m["home"]
    away = m["away"]
    time = m["time"]

    # calcolo probabilità basato su lunghezza nomi squadre (deterministico, non random)
    base = (len(home) + len(away)) % 20

    probability = 50 + base

    if probability > 75:
        probability = 75

    multigol_home = "1-3"
    multigol_away = "0-2"

    over25 = "Possibile"
    btts = "Possibile"

    prediction = {
        "home": home,
        "away": away,
        "league": league,
        "time": time,
        "combo": "Casa o Over 1.5",
        "multigol_home": multigol_home,
        "multigol_away": multigol_away,
        "over25": over25,
        "btts": btts,
        "probability": probability
    }

    # filtro probabilità
    if probability >= 55:
        predictions.append(prediction)

# massimo 30 partite
predictions = predictions[:30]

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=4)

print("Partite analizzate:", len(predictions))
