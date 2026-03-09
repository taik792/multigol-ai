import json
import random

with open("matches.json") as f:
    matches=json.load(f)

predictions=[]

for match in matches:

    home=match["home"]
    away=match["away"]

    avg_goals=random.uniform(2.1,3.6)

    if avg_goals>3:
        multigol="2-4"
        over="Over 2.5"
        probability=round(random.uniform(70,85),1)

    elif avg_goals>2.5:
        multigol="2-3"
        over="Over 2.5"
        probability=round(random.uniform(65,78),1)

    else:
        multigol="1-3"
        over="Under 3.5"
        probability=round(random.uniform(55,68),1)

    home_combo="1-2"
    away_combo="1-2"

    prediction={

        "home":home,
        "away":away,
        "league":match["league"],

        "probability":probability,

        "multigol":multigol,

        "combo_home":home_combo,
        "combo_away":away_combo,

        "over_under":over

    }

    predictions.append(prediction)

with open("predictions.json","w") as f:
    json.dump(predictions,f,indent=4)

print("Predictions created:",len(predictions))
