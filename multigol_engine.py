import json
import math

with open("data/matches.json") as f:
    matches = json.load(f)

with open("data/team_stats.json") as f:
    stats = json.load(f)

def poisson(lmbda, k):
    return (lmbda**k * math.exp(-lmbda)) / math.factorial(k)

predictions = []

for m in matches[:30]:

    home_id = str(m["home_id"])
    away_id = str(m["away_id"])

    # se mancano statistiche usa media globale
    home_attack = stats.get(home_id, {}).get("scored", 1.4)
    home_def = stats.get(home_id, {}).get("conceded", 1.4)

    away_attack = stats.get(away_id, {}).get("scored", 1.4)
    away_def = stats.get(away_id, {}).get("conceded", 1.4)

    home_xg = (home_attack + away_def) / 2
    away_xg = (away_attack + home_def) / 2

    over25_prob = 0
    btts_prob = 0
    multigol_prob = 0

    for h in range(6):
        for a in range(6):

            p = poisson(home_xg, h) * poisson(away_xg, a)

            if h + a > 2:
                over25_prob += p

            if h > 0 and a > 0:
                btts_prob += p

            if 1 <= h + a <= 3:
                multigol_prob += p

    over25 = int(over25_prob * 100)
    btts = int(btts_prob * 100)
    probability = int(multigol_prob * 100)

    total_xg = home_xg + away_xg

    if total_xg < 2:
        multigol = "0-2"
    elif total_xg < 3:
        multigol = "1-3"
    elif total_xg < 4:
        multigol = "2-4"
    else:
        multigol = "3-5"

    if home_xg < 1:
        home_multi = "0-1"
    elif home_xg < 2:
        home_multi = "1-2"
    else:
        home_multi = "2-3"

    if away_xg < 1:
        away_multi = "0-1"
    elif away_xg < 2:
        away_multi = "1-2"
    else:
        away_multi = "2-3"

    predictions.append({
        "home": m["home"],
        "away": m["away"],
        "league": m["league"],
        "multigol": multigol,
        "multigol_home": home_multi,
        "multigol_away": away_multi,
        "over25": over25,
        "btts": btts,
        "probability": probability
    })

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print("Pronostici generati:", len(predictions))