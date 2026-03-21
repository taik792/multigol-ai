import json
import math
import os

# 🔥 Poisson
def poisson(k, lam):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

# carica dati
with open("data/matches_today.json") as f:
    matches = json.load(f)

with open("data/team_stats.json") as f:
    team_stats = json.load(f)

# carica quote manuali (se esiste)
quotes_data = []
if os.path.exists("data/quotes_manual.json"):
    with open("data/quotes_manual.json") as f:
        quotes_data = json.load(f)

predictions = []

# 🔍 funzione per trovare quote match
def find_quotes(home, away):
    for q in quotes_data:
        if q["home"] == home and q["away"] == away:
            return q
    return None

for match in matches:

    home = match["home"]
    away = match["away"]

    home_id = str(match["home_id"])
    away_id = str(match["away_id"])

    # 🔍 controllo se ho quote manuali
    q = find_quotes(home, away)

    # =========================
    # 🔥 ORACLE (QUOTE MANUALI)
    # =========================
    if q:
        try:
            # lambda da quote
            l_home = -math.log(max(0.01, 1 - (1/q["c_o05"])))
            l_away = -math.log(max(0.01, 1 - (1/q["o_o05"])))

            # probabilità combo
            combos = []

            ranges = [(1,3),(1,4),(2,3),(2,4),(2,5)]

            for mi, ma in ranges:
                p_1x = sum(poisson(c, l_home)*poisson(o, l_away)
                           for c in range(6) for o in range(6)
                           if c >= o and mi <= (c+o) <= ma)

                p_x2 = sum(poisson(c, l_home)*poisson(o, l_away)
                           for c in range(6) for o in range(6)
                           if o >= c and mi <= (c+o) <= ma)

                combos.append((p_1x, f"1X + Multigol {mi}-{ma}"))
                combos.append((p_x2, f"X2 + Multigol {mi}-{ma}"))

            combos.sort(key=lambda x: x[0], reverse=True)

            best_prob = combos[0][0] * 100
            best_pick = combos[0][1]

            # 🔥 filtro qualità
            if best_prob >= 65:
                predictions.append({
                    "home": home,
                    "away": away,
                    "league": match["league"],
                    "country": match["country"],
                    "date": match["date"],
                    "time": match["time"],
                    "pick": best_pick,
                    "prob": round(best_prob, 1),
                    "source": "quotes"
                })

        except:
            pass

    # =========================
    # 🤖 AI NORMALE (STATISTICHE)
    # =========================
    else:

        if home_id not in team_stats or away_id not in team_stats:
            continue

        try:
            hf = float(team_stats[home_id]["goals_for"])
            ha = float(team_stats[home_id]["goals_against"])
            af = float(team_stats[away_id]["goals_for"])
            aa = float(team_stats[away_id]["goals_against"])
        except:
            continue

        # lambda base
        l_home = (hf + aa) / 2
        l_away = (af + ha) / 2

        home_win = draw = away_win = 0
        over25 = btts = 0

        for h in range(5):
            for a in range(5):
                p = poisson(h, l_home) * poisson(a, l_away)

                if h > a: home_win += p
                elif h == a: draw += p
                else: away_win += p

                if h + a >= 3: over25 += p
                if h >= 1 and a >= 1: btts += p

        # 🔥 LOGICA SCELTA
        pick = None
        prob = 0

        if home_win > 0.6:
            pick = "1"
            prob = home_win

        elif away_win > 0.6:
            pick = "2"
            prob = away_win

        elif over25 > 0.6:
            pick = "Over 2.5"
            prob = over25

        elif btts > 0.6:
            pick = "Goal"
            prob = btts

        elif over25 < 0.4:
            pick = "Under 2.5"
            prob = 1 - over25

        # 🔥 filtro qualità
        if pick and prob > 0.55:
            predictions.append({
                "home": home,
                "away": away,
                "league": match["league"],
                "country": match["country"],
                "date": match["date"],
                "time": match["time"],
                "pick": pick,
                "prob": round(prob*100, 1),
                "source": "ai"
            })

# 🔥 ordina
predictions = sorted(predictions, key=lambda x: x["prob"], reverse=True)[:10]

print("Pronostici generati:", len(predictions))

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)