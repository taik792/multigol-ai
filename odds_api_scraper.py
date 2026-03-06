import requests
import streamlit as st
from datetime import datetime, timezone, timedelta

API_KEY = st.secrets["ODDS_API_KEY"]

sports = [
    "soccer_epl",
    "soccer_italy_serie_a",
    "soccer_spain_la_liga",
    "soccer_germany_bundesliga",
    "soccer_france_ligue_one"
]


def get_matches():

    matches = []

    now = datetime.now(timezone.utc)
    tomorrow = now + timedelta(days=1)

    for sport in sports:

        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

        params = {
            "apiKey": API_KEY,
            "regions": "eu",
            "markets": "totals,btts",
            "oddsFormat": "decimal"
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
        except:
            continue

        if isinstance(data, dict):
            continue

        for game in data:

            start = datetime.fromisoformat(game["commence_time"].replace("Z","+00:00"))

            # filtro partite oggi + domani
            if start < now or start > tomorrow:
                continue

            home = game.get("home_team")
            away = game.get("away_team")

            over25 = None
            under25 = None
            goal = None
            nogoal = None

            for bookmaker in game.get("bookmakers", []):

                for market in bookmaker.get("markets", []):

                    if market["key"] == "totals":

                        for outcome in market["outcomes"]:

                            if outcome["name"] == "Over" and outcome["point"] == 2.5:
                                over25 = outcome["price"]

                            if outcome["name"] == "Under" and outcome["point"] == 2.5:
                                under25 = outcome["price"]

                    if market["key"] == "btts":

                        for outcome in market["outcomes"]:

                            if outcome["name"] == "Yes":
                                goal = outcome["price"]

                            if outcome["name"] == "No":
                                nogoal = outcome["price"]

            if over25:

                matches.append({

                    "home": home,
                    "away": away,
                    "over25": over25,
                    "under25": under25 if under25 else 2.0,
                    "goal": goal if goal else 1.9,
                    "nogoal": nogoal if nogoal else 1.9

                })

    return matches
