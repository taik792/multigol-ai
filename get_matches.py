import requests
import json
from datetime import datetime

API_KEY="37ddec86e8578a1ff3127d5c394da749"

url="https://v3.football.api-sports.io/fixtures"

headers={
"x-apisports-key":API_KEY
}

today=datetime.now().strftime("%Y-%m-%d")

params={
"date":today,
"timezone":"Europe/Rome"
}

r=requests.get(url,headers=headers,params=params)
data=r.json()

matches=[]

for m in data["response"]:

    if m["fixture"]["status"]["short"]=="NS":

        matches.append({
            "fixture_id":m["fixture"]["id"],
            "home_id":m["teams"]["home"]["id"],
            "away_id":m["teams"]["away"]["id"],
            "home":m["teams"]["home"]["name"],
            "away":m["teams"]["away"]["name"],
            "league":m["league"]["name"],
            "league_id":m["league"]["id"],
            "season":m["league"]["season"]
        })

matches=matches[:10]

with open("matches.json","w") as f:
    json.dump(matches,f,indent=4)

print("Partite salvate:",len(matches))
