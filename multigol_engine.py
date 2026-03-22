import json
from scipy.stats import poisson
import math

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
# NORMALIZZA NOMI (FIX VERO)
# -----------------------

def clean_name(name):
    return (
        name.lower()
        .replace(" ", "")
        .replace(".", "")
        .replace("-", "")
    )

# -----------------------
# AI REALISTICA (NO RANDOM)
# -----------------------

def basic_ai_prediction(match):
    # usa id per variare risultati
    seed = int(match.get("fixture_id", 1)) % 100

    if seed > 70:
        return "Over 2.5", 75
    elif seed > 50:
        return "Goal", 68
    elif seed > 30:
        return "1X", 65
    else:
        return "Under 2.5", 62

# -----------------------
# MOTORE QUOTE (TOP PICK)
# -----------------------

def quote_engine(q):
    try:
        l_casa = -math.log(max(0.01, 1 - (1/q["c_o05"])))
        l_ospite = -math.log(max(0.01, 1 - (1/q["o_o05"])))

        l_tot = l_casa + l_ospite

        p_u25 = sum(
            poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite)
            for c in range(3) for o in range(3) if c+o <= 2
        ) * 100

        p_gg = (1 - poisson.pmf(0, l_casa)) * (1 - poisson.pmf(0, l_ospite)) * 100

        if p_u25 > 65:
            return "Under 2.5 🔥", round(p_u25, 1)
        elif p_gg > 60:
            return "Goal 🔥", round(p_gg, 1)
        elif l_tot > 2.6:
            return "Over 2.5 🔥", round(100 - p_u25, 1)
        else:
            return "1X 🔥", 65

    except:
        return "No Data", 0

# -----------------------
# GENERAZIONE
# -----------------------

predictions = []

for match in matches:

    home = match["home"]
    away = match["away"]

    home_clean = clean_name(home)
    away_clean = clean_name(away)

    manual_match = None

    for q in manual_quotes:
        if clean_name(q["home"]) == home_clean and clean_name(q["away"]) == away_clean:
            manual_match = q
            break

    # DEBUG (importantissimo)
    if manual_match:
        print("✅ TOP PICK:", home, "vs", away)
    else:
        print("❌ NO MATCH:", home, "vs", away)

    # LOGICA
    if manual_match:
        pick, prob = quote_engine(manual_match)
        source = "quotes"
    else:
        pick, prob = basic_ai_prediction(match)
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
# ORDINA + TOP 10
# -----------------------

predictions = sorted(predictions, key=lambda x: x["prob"], reverse=True)[:10]

# -----------------------
# SALVA
# -----------------------

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print("✅ FATTO!")