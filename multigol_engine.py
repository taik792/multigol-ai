import json
import numpy as np
from scipy.stats import poisson

# --- LOAD FILES ---
with open("data/matches_today.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

with open("data/quotes_manual.json", "r", encoding="utf-8") as f:
    manual_quotes = json.load(f)

predictions = []

# --- LOOP MATCHES ---
for match in matches:
    home = match["home"]
    away = match["away"]
    fixture_id = match.get("fixture_id")

    manual_match = None

    # 🔥 MATCH PERFETTO CON ID
    for q in manual_quotes:
        if q.get("fixture_id") == fixture_id:
            manual_match = q
            break

    # =========================
    # 🔴 SE TROVA QUOTE MANUALI
    # =========================
    if manual_match:
        try:
            q1 = manual_match["q1"]
            qx = manual_match["qx"]
            q2 = manual_match["q2"]

            qgg = manual_match["qgg"]
            qng = manual_match["qng"]

            c_o05 = manual_match["c_o05"]
            c_o15 = manual_match["c_o15"]

            o_o05 = manual_match["o_o05"]
            o_o15 = manual_match["o_o15"]

            # --- CALCOLO LAMBDA ---
            l_home = -np.log(max(0.01, 1 - (1 / c_o05)))
            l_away = -np.log(max(0.01, 1 - (1 / o_o05)))
            l_tot = l_home + l_away

            # --- PROBABILITÀ ---
            p_over25 = 100 - sum(
                poisson.pmf(c, l_home) * poisson.pmf(o, l_away)
                for c in range(3)
                for o in range(3)
                if c + o <= 2
            ) * 100

            p_gg = (1 - poisson.pmf(0, l_home)) * (1 - poisson.pmf(0, l_away)) * 100

            # --- SCELTA PRONOSTICO ---
            if p_over25 > 65:
                pick = "Over 2.5"
                prob = p_over25
            elif p_gg > 60:
                pick = "GG"
                prob = p_gg
            elif l_tot < 2:
                pick = "Under 2.5"
                prob = 70
            else:
                pick = "1X"
                prob = 65

            predictions.append({
                "home": home,
                "away": away,
                "league": match.get("league", ""),
                "date": match.get("date", ""),
                "time": match.get("time", ""),
                "pick": pick,
                "prob": round(prob, 1),
                "source": "quotes"
            })

            print(f"✅ TOP PICK: {home} vs {away}")

        except Exception as e:
            print("Errore manual match:", e)

    # =========================
    # 🔵 AI AUTOMATICO
    # =========================
    else:
        try:
            # valori base AI
            l_home = 1.2
            l_away = 1.0
            l_tot = l_home + l_away

            p_over25 = 100 - sum(
                poisson.pmf(c, l_home) * poisson.pmf(o, l_away)
                for c in range(3)
                for o in range(3)
                if c + o <= 2
            ) * 100

            p_gg = (1 - poisson.pmf(0, l_home)) * (1 - poisson.pmf(0, l_away)) * 100

            # logica migliorata
            if p_over25 > 60:
                pick = "Over 2.5"
                prob = p_over25
            elif p_gg > 55:
                pick = "GG"
                prob = p_gg
            elif l_tot < 2:
                pick = "Under 2.5"
                prob = 65
            else:
                pick = "1X"
                prob = 60

            predictions.append({
                "home": home,
                "away": away,
                "league": match.get("league", ""),
                "date": match.get("date", ""),
                "time": match.get("time", ""),
                "pick": pick,
                "prob": round(prob, 1),
                "source": "ai"
            })

        except Exception as e:
            print("Errore AI:", e)

# --- SALVA OUTPUT ---
with open("data/predictions.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, indent=2)

print("✅ Predictions generate!")