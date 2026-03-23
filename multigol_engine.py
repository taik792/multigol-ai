import json

with open("data/matches_today.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

predictions = []

for match in matches:

    home = match.get("home")
    away = match.get("away")

    # logica semplice ma reale
    # usa differenza ranking/forma se disponibile

    try:
        home_goals = match.get("home_goals_avg", 1.2)
        away_goals = match.get("away_goals_avg", 1.0)
    except:
        home_goals = 1.2
        away_goals = 1.0

    total_goals = home_goals + away_goals

    # scelte realistiche
    if total_goals >= 2.5:
        pick = "Over 2.5"
        prob = 65
    elif home_goals > away_goals:
        pick = "1"
        prob = 60
    else:
        pick = "GG"
        prob = 58

    predictions.append({
        "home": home,
        "away": away,
        "prediction": pick,
        "probability": prob
    })

# ordina
predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)

# top
top_picks = predictions[:5]

with open("predictions.json", "w", encoding="utf-8") as f:
    json.dump({
        "all": predictions,
        "top": top_picks
    }, f, indent=2)

print(f"Generate: {len(predictions)}")