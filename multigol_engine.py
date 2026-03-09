import json

with open("matches.json","r",encoding="utf-8") as f:
    matches=json.load(f)

predictions=[]

for match in matches:

    home=match["home"]
    away=match["away"]

    strength_home=len(home)
    strength_away=len(away)

    diff=abs(strength_home-strength_away)

    probability=60+(10-diff)

    if probability>85:
        probability=85

    if strength_home>strength_away:
        combo="Casa"
    elif strength_home<strength_away:
        combo="Ospite"
    else:
        combo="Equilibrio"

    if diff<=2:
        multigol_home="1-2"
        multigol_away="1-2"
    elif diff<=5:
        multigol_home="1-3"
        multigol_away="0-2"
    else:
        multigol_home="2-4"
        multigol_away="0-1"

    if probability>70:
        over25="Yes"
        btts="Yes"
    else:
        over25="No"
        btts="No"

    predictions.append({
        "home":home,
        "away":away,
        "league":match["league"],
        "combo":combo,
        "multigol_home":multigol_home,
        "multigol_away":multigol_away,
        "over25":over25,
        "btts":btts,
        "probability":probability
    })

with open("predictions.json","w",encoding="utf-8") as f:
    json.dump(predictions,f,indent=4,ensure_ascii=False)

print("Predictions created:",len(predictions))
