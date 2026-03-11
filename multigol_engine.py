import json
import math

with open("data/matches_today.json") as f:
 matches = json.load(f)

with open("data/teams_stats.json") as f:
 stats = json.load(f)

predictions = []

def poisson(lam,k):
 return (lam**k * math.exp(-lam)) / math.factorial(k)

for m in matches:

 home_stats = stats.get(str(m["home_id"]))
 away_stats = stats.get(str(m["away_id"]))

 if not home_stats or not away_stats:
  continue

 home_xg = (home_stats["scored"] + away_stats["conceded"]) / 2
 away_xg = (away_stats["scored"] + home_stats["conceded"]) / 2

 over25 = 0
 btts = 0

 for h in range(6):
  for a in range(6):

   p = poisson(home_xg,h) * poisson(away_xg,a)

   if h+a >=3:
    over25 += p

   if h>0 and a>0:
    btts += p

 prob = round((over25+btts)/2*100)

 predictions.append({

  "home": m["home"],
  "away": m["away"],
  "league": m["league"],
  "country": m["country"],
  "time": m["time"],

  "over25": round(over25*100),
  "btts": round(btts*100),
  "probability": prob

 })

with open("data/predictions.json","w") as f:
 json.dump(predictions,f,indent=2)