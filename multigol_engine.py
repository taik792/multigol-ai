import json
import random

# Carica partite
with open("data/matches_today.json", "r") as f:
    matches = json.load(f)

predictions = {
    "top": [],
    "all": []
}

def generate_pick():
    picks = [
        "Over 1.5",
        "Over 2.5",
        "GG",
        "Over 1.5 + GG",
        "Multigol 1-3",
        "Multigol 2-4"
    ]
    return random.choice(picks)

for match in matches:
    try:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        league = match["league"]["name"]
        date = match["fixture"]["date"]

        pick = generate_pick()

        game = {
            "home": home,
            "away": away,
            "league": league,
            "date": date,
            "pick": pick  # 🔥 QUESTO ERA IL PROBLEMA
        }

        predictions["all"].append(game)

    except Exception as e:
        print("Errore match:", e)

# 🔥 TOP PICKS (prime 5)
predictions["top"] = predictions["all"][:5]

# Salva file
with open("data/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print("✅ Generate", len(predictions["all"]), "predictions")