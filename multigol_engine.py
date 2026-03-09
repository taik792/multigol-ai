import json
from datetime import datetime

with open("matches.json","r",encoding="utf-8") as f:
    matches=json.load(f)

predictions=[]

for match in matches:

    home=match["home"]
    away=match["away"]
    date=match.get("date","")

    # valori medi realistici base
    home_attack=1.6
    home_defense=1.2

    away_attack=1.4
    away_defense=1.3

    # expected goals stimati
    home_xg=(home_attack+away_defense)/2
    away_xg=(away_attack+home_defense)/2

    total_goals=home_xg+away_xg

    # probabilità over
    over_prob=min(90,round(total_goals/4*100))

    # probabilità btts
    btts_prob=min(85,round((home_xg*away_xg)/2*100))

    # multigol casa
    if home_xg<1:
        home_range="0-1"
    elif home_xg<2:
        home_range="1-2"
    else:
        home_range="1-3"

    # multigol ospite
    if away_xg<1:
        away_range="0-1"
    elif away_xg<2:
        away_range="1-2"
    else:
        away_range="1-3"

    prediction={

        "home":home,
        "away":away,
        "date":date,

        "multigol_home":home_range,
        "multigol_away":away_range,

        "over25_prob":over_prob,
        "btts_prob":btts_prob

    }

    predictions.append(prediction)

with open("predictions.json","w",encoding="utf-8") as f:
    json.dump(predictions,f,indent=4,ensure_ascii=False)

print("Predictions created:",len(predictions))
