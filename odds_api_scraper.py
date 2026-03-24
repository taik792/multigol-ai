import requests
import json

API_KEY = "LA_TUA_API_KEY"

with open("data/matches.json") as f:
    matches = json.load(f)

headers = {
    "x-apisports-key": API_KEY
}

odds_data = {}

for m in matches:
    fixture_id = m["fixture"]["id"]

    url = f"https://v3.football.api-sports.io/odds?fixture={fixture_id}"

    res = requests.get(url, headers=headers).json()

    if not res["response"]:
        continue

    try:
        bookmakers = res["response"][0]["bookmakers"]
        bets = bookmakers[0]["bets"]

        over_15 = None
        over_25 = None

        for b in bets:
            if b["name"] == "Goals Over/Under":
                for v in b["values"]:
                    if v["value"] == "Over 1.5":
                        over_15 = float(v["odd"])
                    if v["value"] == "Over 2.5":
                        over_25 = float(v["odd"])

        if over_15 and over_25:
            odds_data[str(fixture_id)] = {
                "over_1_5": over_15,
                "over_2_5": over_25
            }

    except:
        continue

with open("odds.json", "w") as f:
    json.dump(odds_data, f, indent=2)

print("Odds salvate:", len(odds_data))