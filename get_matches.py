import requests
import json
import os
from datetime import datetime, timedelta

# 🔐 API da GitHub Secrets
API_KEY = os.getenv("API_FOOTBALL_KEY")

BASE_URL = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

def get_matches():
    matches = []

    today = datetime.now()
    dates = [
        today.strftime("%Y-%m-%d"),
        (today + timedelta(days=1)).strftime("%Y-%m-%d")
    ]

    for date in dates:
        url = f"{BASE_URL}?date={date}"

        response = requests.get(url, headers=headers)
        data = response.json()

        print("DEBUG:", data)  # 🔍 fondamentale

        if "response" not in data:
            print("❌ Errore API")
            continue

        for match in data["response"]:
            status = match["fixture"]["status"]["short"]

            if status in ["NS", "TBD"]:
                matches.append({
                    "fixture_id": match["fixture"]["id"],
                    "home": match["teams"]["home"]["name"],
                    "away": match["teams"]["away"]["name"],
                    "date": match["fixture"]["date"]
                })

    # ⚠️ fallback
    if not matches:
        print("⚠️ Nessuna partita trovata")

    # salva file
    with open("matches.json", "w") as f:
        json.dump(matches, f, indent=2)

    with open("data/matches_today.json", "w") as f:
        json.dump(matches, f, indent=2)

    print(f"✅ Partite trovate: {len(matches)}")

if __name__ == "__main__":
    get_matches()