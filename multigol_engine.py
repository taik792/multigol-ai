import json
import math

# funzione Poisson
def poisson(k, lam):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

# carica dati
with open("data/matches_today.json") as f:
    matches = json.load(f)

with open("data/team_stats.json") as f:
    team_stats = json.load(f)

predictions = []

for match in matches:

    home_id = str(match["home_id"])
    away_id = str(match["away_id"])

    if home_id not in team_stats or away_id not in team_stats:
        continue

    try:
        home_for = float(team_stats[home_id]["goals_for"])
        home_against = float(team_stats[home_id]["goals_against"])
        away_for = float(team_stats[away_id]["goals_for"])
        away_against = float(team_stats[away_id]["goals_against"])
    except:
        continue

    # 🔥 Expected goals
    home_lambda = (home_for + away_against) / 2
    away_lambda = (away_for + home_against) / 2

    score_probs = {}

    # calcolo probabilità risultati
    for h in range(6):
        for a in range(6):
            p = poisson(h, home_lambda) * poisson(a, away_lambda)
            score_probs[(h, a)] = p

    home_win = 0
    draw = 0
    away_win = 0
    btts = 0
    over25 = 0
    multigol_2_5 = 0

    for (h, a), p in score_probs.items():

        if h > a:
            home_win += p
        elif h == a:
            draw += p
        else:
            away_win += p

        if h >= 1 and a >= 1:
            btts += p

        if h + a >= 3:
            over25 += p

        if 2 <= (h + a) <= 5:
            multigol_2_5 += p

    # 🔥 Over squadra
    home_over05 = 1 - poisson(0, home_lambda)
    home_over15 = 1 - (poisson(0, home_lambda) + poisson(1, home_lambda))

    away_over05 = 1 - poisson(0, away_lambda)
    away_over15 = 1 - (poisson(0, away_lambda) + poisson(1, away_lambda))

    # 🔥 Favorita
    if home_win > away_win:
        favorite = "home"
    else:
        favorite = "away"

    # 🔥 Combo intelligente
    combo = ""

    if favorite == "home":
        if home_win + draw > 0.65 and multigol_2_5 > 0.55:
            combo = "1X + Multigol 2-5"
        elif home_over15 > 0.6:
            combo = "Over 1.5 Casa"
    else:
        if away_win + draw > 0.65 and multigol_2_5 > 0.55:
            combo = "X2 + Multigol 2-5"
        elif away_over15 > 0.6:
            combo = "Over 1.5 Ospite"

    # 🔥 filtro qualità
    if multigol_2_5 < 0.43:
        continue

    predictions.append({
        "home": match["home"],
        "away": match["away"],
        "league": match["league"],
        "country": match["country"],
        "date": match["date"],
        "time": match["time"],

        "home_win": round(home_win * 100, 1),
        "draw": round(draw * 100, 1),
        "away_win": round(away_win * 100, 1),

        "btts": round(btts * 100, 1),
        "over25": round(over25 * 100, 1),
        "multigol": "2-5",

        "home_over05": round(home_over05 * 100, 1),
        "home_over15": round(home_over15 * 100, 1),
        "away_over05": round(away_over05 * 100, 1),
        "away_over15": round(away_over15 * 100, 1),

        "combo": combo
    })

# 🔥 TOP 10
predictions = sorted(predictions, key=lambda x: x["over25"], reverse=True)[:10]

print("Pronostici generati:", len(predictions))

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)
