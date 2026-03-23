import json
import math

# ========================
# CONFIG
# ========================
TOP_THRESHOLD = 0.70   # minimo per top pick
MIN_MATCHES = 3        # minimo partite giocate

# ========================
# LOAD FILES
# ========================
with open("data/matches_today.json", "r") as f:
    matches = json.load(f)

with open("data/teams_stats.json", "r") as f:
    stats = json.load(f)

# ========================
# HELPER
# ========================
def poisson_prob(lmbda, k):
    return (lmbda ** k * math.exp(-lmbda)) / math.factorial(k)

def over25_prob(home_avg, away_avg):
    lmbda = home_avg + away_avg
    prob = 0
    for i in range(3):
        for j in range(3 - i):
            prob += poisson_prob(home_avg, i) * poisson_prob(away_avg, j)
    return 1 - prob

def btts_prob(home_avg, away_avg):
    p_home = 1 - poisson_prob(home_avg, 0)
    p_away = 1 - poisson_prob(away_avg, 0)
    return p_home * p_away

# ========================
# MAIN
# ========================
all_preds = []

for match in matches:
    home_id = str(match["home_id"])
    away_id = str(match["away_id"])

    if home_id not in stats or away_id not in stats:
        continue

    home = stats[home_id]
    away = stats[away_id]

    if home["played"] < MIN_MATCHES or away["played"] < MIN_MATCHES:
        continue

    home_avg = home["goals_for"] / home["played"]
    away_avg = away["goals_for"] / away["played"]

    # Probabilità
    over25 = over25_prob(home_avg, away_avg)
    btts = btts_prob(home_avg, away_avg)

    # 1X semplice
    home_strength = home_avg
    away_strength = away_avg

    prob_1x = home_strength / (home_strength + away_strength)

    # scegli pick migliore
    best_pick = None
    best_prob = 0

    options = {
        "Over 2.5": over25,
        "GG": btts,
        "1X": prob_1x
    }

    for k, v in options.items():
        if v > best_prob:
            best_prob = v
            best_pick = k

    if best_prob < 0.55:
        continue

    prediction = {
        "fixture_id": match["fixture_id"],
        "home": match["home"],
        "away": match["away"],
        "pick": best_pick,
        "probability": round(best_prob * 100, 1)
    }

    all_preds.append(prediction)

# ========================
# TOP PICKS
# ========================
top_preds = [p for p in all_preds if p["probability"] >= TOP_THRESHOLD * 100]

# prendi i migliori 5
top_preds = sorted(top_preds, key=lambda x: x["probability"], reverse=True)[:5]

# ========================
# SAVE
# ========================
output = {
    "all": all_preds,
    "top": top_preds
}

with open("predictions.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Predizioni: {len(all_preds)}")
print(f"Top picks: {len(top_preds)}")