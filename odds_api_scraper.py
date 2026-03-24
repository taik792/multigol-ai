import requests, json, os, time

API_KEY = os.getenv("API_KEY")
headers = {"x-apisports-key": API_KEY}

with open("data/matches.json") as f:
    matches = json.load(f)

odds = {}

for m in matches:
    fixture_id = m["fixture_id"]

    url = f"https://v3.football.api-sports.io/odds?fixture={fixture_id}"

    res = requests.get(url, headers=headers).json()

    if not res.get("response"):
        continue

    try:
        bets = res["response"][0]["bookmakers"][0]["bets"]

        over15, over25 = None, None

        for b in bets:
            if b["name"] == "Goals Over/Under":
                for v in b["values"]:
                    if v["value"] == "Over 1.5":
                        over15 = float(v["odd"])
                    if v["value"] == "Over 2.5":
                        over25 = float(v["odd"])

        if over15 and over25:
            odds[str(fixture_id)] = {
                "over_1_5": over15,
                "over_2_5": over25
            }

    except:
        continue

    time.sleep(1.1)  # evita blocco API

with open("data/odds.json", "w") as f:
    json.dump(odds, f, indent=2)

print("Odds:", len(odds))