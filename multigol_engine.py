import json
import math

# --- funzione Poisson ---
def poisson(k, lam):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

# --- carica dati ---
with open("data/matches_today.json") as f:
    matches = json.load(f)

with open("data/team_stats.json") as f:
    team_stats = json.load(f)

# --- carica quote manuali ---
try:
    with open("data/quotes_manual.json") as f:
        manual_quotes = json.load(f)
except:
    manual_quotes = []

predictions = []

for match in matches:

    home = match["home"]
    away = match["away"]

    # --- MATCH QUOTE MANUALI ---
    manual_match = None
    for q in manual_quotes:
        if q["home"].strip().lower() == home.strip().lower() and \
           q["away"].strip().lower() == away.strip().lower():
            manual_match = q
            break

    # --- SE TROVA MATCH MANUALE ---
    if manual_match:
        predictions.append({
            "home": home,
            "away": away,
            "league": match["league"],
            "country": match["country"],
            "date": match["date"],
            "time": match["time"],
            "pick": "Combo da Quote",
            "prob": 85,
            "source": "quotes"
        })
        continue

    # --- AI STANDARD ---
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

    # --- lambda ---
    home_lambda = (home_for + away_against) / 2
    away_lambda = (away_for + home_against) / 2

    score_probs = {}

    for h in range(6):
        for a in range(6):
            p = poisson(h, home_lambda) * poisson(a, away_lambda)
            score_probs[(h, a)] = p

    home_win = draw = away_win = 0
    over25 = under25 = 0

    for (h, a), p in score_probs.items():
        if h > a:
            home_win += p
        elif h == a:
            draw += p
        else:
            away_win += p

        if h + a >= 3:
            over25 += p
        else:
            under25 += p

    # --- scelta pronostico ---
    if over25 > 0.60:
        pick = "Over 2.5"
        prob = over25
    elif under25 > 0.60:
        pick = "Under 2.5"
        prob = under25
    elif home_win > 0.50:
        pick = "1"
        prob = home_win
    elif away_win > 0.50:
        pick = "2"
        prob = away_win
    else:
        continue

    predictions.append({
        "home": home,
        "away": away,
        "league": match["league"],
        "country": match["country"],
        "date": match["date"],
        "time": match["time"],
        "pick": pick,
        "prob": round(prob * 100, 1),
        "source": "ai"
    })

# --- SEPARA ---
quotes_matches = [p for p in predictions if p["source"] == "quotes"]
ai_matches = [p for p in predictions if p["source"] == "ai"]

# --- SOLO TOP 10 AI ---
ai_matches = sorted(ai_matches, key=lambda x: x["prob"], reverse=True)[:10]

# --- UNISCI ---
final_predictions = quotes_matches + ai_matches

print("TOP PICK:", len(quotes_matches))
print("AI MATCHES:", len(ai_matches))

# --- salva ---
with open("data/predictions.json", "w") as f:
    json.dump(final_predictions, f, indent=2)