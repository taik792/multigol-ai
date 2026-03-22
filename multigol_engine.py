import json
import numpy as np
from scipy.stats import poisson

# -----------------------
# CARICA FILE
# -----------------------

with open("data/matches_today.json") as f:
    matches = json.load(f)

try:
    with open("data/quotes_manual.json") as f:
        manual_quotes = json.load(f)
except:
    manual_quotes = []

# -----------------------
# FUNZIONE PULIZIA NOMI
# -----------------------

def clean_name(name):
    return name.lower().strip().replace(" ", "")

# -----------------------
# AI BASE (senza quote)
# -----------------------

def basic_ai_prediction():
    # simulazione semplice
    p = np.random.randint(55, 80)

    if p > 70:
        return "Over 2.5", p
    elif p > 60:
        return "Goal", p
    else:
        return "Under 2.5", p

# -----------------------
# MOTORE QUOTE (IL TUO)
# -----------------------

def quote_engine(q):
    try:
        l_casa = -np.log(max(0.01, 1 - (1/q["c_o05"])))
        l_ospite = -np.log(max(0.01, 1 - (1/q["o_o05"])))

        l_tot = l_casa + l_ospite

        p_u25 = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite)
                    for c in range(3) for o in range(3) if c+o <= 2) * 100

        p_gg = (1 - poisson.pmf(0, l_casa)) * (1 - poisson.pmf(0, l_ospite)) * 100

        # scelta intelligente
        if p_u25 > 60:
            return "Under 2.5", round(p_u25, 1)
        elif p_gg > 60:
            return "Goal", round(p_gg, 1)
        elif l_tot > 2.5:
            return "Over 2.5", round(100 - p_u25, 1)
        else:
            return "1X", 65

    except:
        return "No Data", 0

# -----------------------
# GENERAZIONE PRONOSTICI
# -----------------------

predictions = []

for match in matches:

    home = match["home"]
    away = match["away"]

    # cerca nelle quote manuali
    manual_match = None

    for q in manual_quotes:
        if clean_name(q["home"]) == clean_name(home) and \
           clean_name(q["away"]) == clean_name(away):
            manual_match = q
            break

    # DEBUG
    if manual_match:
        print("✅ MATCH TROVATO:", home, "vs", away)
    else:
        print("❌ NO MATCH:", home, "vs", away)

    # LOGICA
    if manual_match:
        pick, prob = quote_engine(manual_match)
        source = "quotes"
    else:
        pick, prob = basic_ai_prediction()
        source = "ai"

    predictions.append({
        "home": home,
        "away": away,
        "league": match["league"],
        "date": match["date"],
        "time": match["time"],
        "pick": pick,
        "prob": prob,
        "source": source
    })

# -----------------------
# LIMITA A 10 PARTITE
# -----------------------

predictions = sorted(predictions, key=lambda x: x["prob"], reverse=True)[:10]

# -----------------------
# SALVA OUTPUT
# -----------------------

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print("✅ PRONOSTICI GENERATI!")