import json
import math

# funzione Poisson
def poisson_prob(lmbda, k):
    return (lmbda ** k * math.exp(-lmbda)) / math.factorial(k)

# carica dati
with open("data/matches.json") as f:
    matches = json.load(f)

with open("data/team_stats.json") as f:
    stats = json.load(f)

predictions = []

for match in matches:

    home = match["home"]
    away = match["away"]

    if home not in stats or away not in stats:
        continue

    home_stats = stats[home]
    away_stats = stats[away]

    # medie gol
    home_scored = home_stats["goals_scored"]
    home_conceded = home_stats["goals_conceded"]

    away_scored = away_stats["goals_scored"]
    away_conceded = away_stats["goals_conceded"]

    # expected goals
    xg_home = (home_scored + away_conceded) / 2
    xg_away = (away_scored + home_conceded) / 2

    # probabilità gol
    home_probs = [poisson_prob(xg_home, i) for i in range(6)]
    away_probs = [poisson_prob(xg_away, i) for i in range(6)]

    # Over 2.5
    over25 = 0
    for i in range(6):
        for j in range(6):
            if i + j >= 3:
                over25 += home_probs[i] * away_probs[j]

    # BTTS
    btts = 0
    for i in range(1,6):
        for j in range(1,6):
            btts += home_probs[i] * away_probs[j]

    # Multigol casa
    mg_home_13 = sum(home_probs[1:4])
    mg_home_14 = sum(home_probs[1:5])
    mg_home_24 = sum(home_probs[2:5])

    # Multigol ospite
    mg_away_02 = sum(away_probs[0:3])
    mg_away_13 = sum(away_probs[1:4])
    mg_away_14 = sum(away_probs[1:5])

    # selezione migliore
    mg_home = max([
        ("1-3", mg_home_13),
        ("1-4", mg_home_14),
        ("2-4", mg_home_24)
    ], key=lambda x: x[1])

    mg_away = max([
        ("0-2", mg_away_02),
        ("1-3", mg_away_13),
        ("1-4", mg_away_14)
    ], key=lambda x: x[1])

    predictions.append({
        "home": home,
        "away": away,
        "over25": round(over25*100,1),
        "btts": round(btts*100,1),
        "multigol_home": mg_home[0],
        "multigol_home_prob": round(mg_home[1]*100,1),
        "multigol_away": mg_away[0],
        "multigol_away_prob": round(mg_away[1]*100,1)
    })

# salva pronostici
with open("data/predictions.json", "w") as f:
    json.dump(predictions[:30], f, indent=2)

print("Pronostici generati:", len(predictions[:30]))