import json
import math

# funzione Poisson
def poisson(lmbda, k):
    return (lmbda ** k) * math.exp(-lmbda) / math.factorial(k)

# carica partite
with open("matches.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    # goal medi (devono arrivare dalle statistiche API)
    home_attack = m.get("home_attack", 1.5)
    away_attack = m.get("away_attack", 1.2)

    home_def = m.get("home_def", 1.2)
    away_def = m.get("away_def", 1.4)

    # goal attesi
    home_xg = (home_attack + away_def) / 2
    away_xg = (away_attack + home_def) / 2

    prob_home = 0
    prob_draw = 0
    prob_away = 0

    prob_over25 = 0
    prob_btts = 0

    goal_probs = {}

    for i in range(6):
        for j in range(6):

            p = poisson(home_xg, i) * poisson(away_xg, j)
            goal_probs[(i, j)] = p

            if i > j:
                prob_home += p
            elif i == j:
                prob_draw += p
            else:
                prob_away += p

            if i + j > 2:
                prob_over25 += p

            if i > 0 and j > 0:
                prob_btts += p

    # multigol
    multigol_probs = {
        "1-3": sum(p for (i, j), p in goal_probs.items() if 1 <= i+j <= 3),
        "2-4": sum(p for (i, j), p in goal_probs.items() if 2 <= i+j <= 4),
        "2-5": sum(p for (i, j), p in goal_probs.items() if 2 <= i+j <= 5),
    }

    best_multigol = max(multigol_probs, key=multigol_probs.get)

    # multigol casa
    home_goals = sum(i * poisson(home_xg, i) for i in range(5))

    if home_goals < 1.2:
        multigol_home = "0-2"
    elif home_goals < 2:
        multigol_home = "1-2"
    else:
        multigol_home = "1-3"

    # multigol ospite
    away_goals = sum(i * poisson(away_xg, i) for i in range(5))

    if away_goals < 1.2:
        multigol_away = "0-2"
    elif away_goals < 2:
        multigol_away = "1-2"
    else:
        multigol_away = "1-3"

    # esito
    if prob_home > prob_draw and prob_home > prob_away:
        esito = "1"
    elif prob_away > prob_draw:
        esito = "2"
    else:
        esito = "X"

    prediction = {
        "home": home,
        "away": away,
        "esito": esito,
        "prob_1": round(prob_home * 100, 1),
        "prob_x": round(prob_draw * 100, 1),
        "prob_2": round(prob_away * 100, 1),
        "multigol": best_multigol,
        "multigol_home": multigol_home,
        "multigol_away": multigol_away,
        "over25": round(prob_over25 * 100, 1),
        "btts": round(prob_btts * 100, 1)
    }

    predictions.append(prediction)

# salva
with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, indent=4, ensure_ascii=False)

print("Predictions created:", len(predictions))
