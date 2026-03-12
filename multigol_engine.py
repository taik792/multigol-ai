import json
import random

# carica partite
with open("matches.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

# carica statistiche squadre
try:
    with open("teams_stats.json", "r", encoding="utf-8") as f:
        stats = json.load(f)
except:
    stats = {}

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    # statistiche squadra casa
    home_scored = stats.get(home, {}).get("scored", random.uniform(1.1,2.0))
    home_conceded = stats.get(home, {}).get("conceded", random.uniform(0.9,1.8))

    # statistiche squadra trasferta
    away_scored = stats.get(away, {}).get("scored", random.uniform(1.0,1.9))
    away_conceded = stats.get(away, {}).get("conceded", random.uniform(1.0,2.0))

    # gol attesi
    home_expected = (home_scored + away_conceded) / 2
    away_expected = (away_scored + home_conceded) / 2

    total_goals = home_expected + away_expected

    # calcolo percentuali
    over25 = int(min(95, max(30, total_goals * 35)))
    btts = int(min(90, max(25, (home_expected * away_expected) * 25)))

    probability = int((over25 * 0.6) + (btts * 0.4))

    predictions.append({
        "home": home,
        "away": away,
        "league": m["league"],
        "country": m["country"],
        "time": m["time"],
        "over25": over25,
        "btts": btts,
        "probability": probability
    })

# ordina per probabilità
predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)

# salva risultati
with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, indent=2)

print("Pronostici generati:", len(predictions))