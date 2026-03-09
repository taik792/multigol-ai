import json
import requests
import math

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
"x-apisports-key": API_KEY
}

def poisson(k,lam):
    return (lam**k*math.exp(-lam))/math.factorial(k)

with open("matches.json","r") as f:
    matches=json.load(f)

predictions=[]

for match in matches:

    home=match["home"]
    away=match["away"]
    league=match["league"]
    time=match["time"]

    home_id=match["home_id"]
    away_id=match["away_id"]
    league_id=match["league_id"]
    fixture_id=match["fixture_id"]

    try:

        url_home=f"https://v3.football.api-sports.io/teams/statistics?league={league_id}&season=2024&team={home_id}"
        url_away=f"https://v3.football.api-sports.io/teams/statistics?league={league_id}&season=2024&team={away_id}"

        home_stats=requests.get(url_home,headers=headers).json()
        away_stats=requests.get(url_away,headers=headers).json()

        home_scored=float(home_stats["response"]["goals"]["for"]["average"]["home"])
        home_conceded=float(home_stats["response"]["goals"]["against"]["average"]["home"])

        away_scored=float(away_stats["response"]["goals"]["for"]["average"]["away"])
        away_conceded=float(away_stats["response"]["goals"]["against"]["average"]["away"])

        url_odds=f"https://v3.football.api-sports.io/odds?fixture={fixture_id}"

        odds=requests.get(url_odds,headers=headers).json()

        over_prob=0
        btts_prob=0

        for bookmaker in odds["response"]:

            for bet in bookmaker["bookmakers"][0]["bets"]:

                if bet["name"]=="Over/Under":

                    for value in bet["values"]:

                        if value["value"]=="Over 2.5":

                            over_prob=1/float(value["odd"])

                if bet["name"]=="Both Teams Score":

                    for value in bet["values"]:

                        if value["value"]=="Yes":

                            btts_prob=1/float(value["odd"])

    except:
        continue

    expected_home=(home_scored+away_conceded)/2
    expected_away=(away_scored+home_conceded)/2

    home_probs=[poisson(i,expected_home) for i in range(6)]
    away_probs=[poisson(i,expected_away) for i in range(6)]

    poisson_over=0

    for h in range(6):
        for a in range(6):

            if h+a>=3:
                poisson_over+=home_probs[h]*away_probs[a]

    final_over=(poisson_over+over_prob)/2
    final_btts=(btts_prob)/1

    multigol_home="1-3" if expected_home>=1 else "0-2"
    multigol_away="1-3" if expected_away>=1 else "0-2"

    combo="Casa" if expected_home>expected_away else "Ospite"

    probability=round(max(final_over,final_btts)*100)

    predictions.append({

        "home":home,
        "away":away,
        "league":league,
        "time":time,
        "combo":combo,
        "multigol_home":multigol_home,
        "multigol_away":multigol_away,
        "over25":"Yes" if final_over>0.5 else "No",
        "btts":"Yes" if final_btts>0.5 else "No",
        "probability":probability

    })

with open("predictions.json","w") as f:
    json.dump(predictions,f,indent=4)

print("Predictions created:",len(predictions))