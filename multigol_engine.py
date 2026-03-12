import json
import math

# carica partite
with open("data/matches.json") as f:
    matches = json.load(f)

# carica statistiche squadre
with open("data/team_stats.json") as f:
    stats = json.load(f)

predictions = []

def poisson(lmbda, k):
    return (lmbda ** k * math.exp(-lmbda)) / math.factorial(k)

for match in matches:

    home = match["home"]
    away = match["away"]
    league = match["league"]

    if home not in stats or away not in stats:
        continue

    home_stats = stats[home]
    away_stats = stats[away]

    home_scored = home_stats["goals_for"]
    home_conceded = home_stats["goals_against"]

    away_scored = away_stats["goals_for"]
    away_conceded = away_stats["goals_against"]

    home_attack = (home_scored + away_conceded) / 2
    away_attack = (away_scored + home_conceded) / 2

    probs = {}

    for i in range(6):
        for j in range(6):
            p = poisson(home_attack, i) * poisson(away_attack, j)
            probs[(i,j)] = p

    over15 = sum(p for (i,j),p in probs.items() if i+j >= 2)
    over25 = sum(p for (i,j),p in probs.items() if i+j >= 3)
    btts = sum(p for (i,j),p in probs.items() if i>0 and j>0)

    home_goals = [0]*6
    away_goals = [0]*6

    for (i,j),p in probs.items():
        home_goals[i] += p
        away_goals[j] += p

    def multigol_range(goals):

        mg = {
            "0-1": goals[0] + goals[1],
            "1-3": goals[1] + goals[2] + goals[3],
            "2-4": goals[2] + goals[3] + goals[4],
            "2-5": goals[2] + goals[3] + goals[4] + goals[5],
            "3-6": goals[3] + goals[4] + goals[5]
        }

        best = max(mg, key=mg.get)
        prob = mg[best]

        return best, round(prob*100,1)

    mg_home, prob_home = multigol_range(home_goals)
    mg_away, prob_away = multigol_range(away_goals)

    prediction = {
        "league": league,
        "home": home,
        "away": away,
        "over15": round(over15*100,1),
        "over25": round(over25*100,1),
        "btts": round(btts*100,1),
        "multigol_home": mg_home,
        "multigol_home_prob": prob_home,
        "multigol_away": mg_away,
        "multigol_away_prob": prob_away
    }

    predictions.append(prediction)

# ordina per probabilità
predictions = sorted(
    predictions,
    key=lambda x: x["multigol_home_prob"] + x["multigol_away_prob"],
    reverse=True
)

# prende le migliori 30
predictions = predictions[:30]

# salva nel posto corretto per il sito
with open("data/predictions.json","w") as f:
    json.dump(predictions, f, indent=4)

print("Pronostici generati:", len(predictions))