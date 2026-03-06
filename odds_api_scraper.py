import requests
import streamlit as st
from datetime import datetime, timezone, timedelta

API_KEY = st.secrets["ODDS_API_KEY"]

sports = [
    "soccer_epl",
    "soccer_italy_serie_a",
    "soccer_spain_la_liga",
    "soccer_germany_bundesliga",
    "soccer_france_ligue_one",
    "soccer_netherlands_eredivisie",
    "soccer_portugal_primeira_liga",
    "soccer_turkey_super_league"
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

            commence = game.get("commence_time")

            if not commence:
                continue

            start = datetime.fromisoformat(commence.replace("Z","+00:00"))

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

                    if market.get("key") == "totals":

                        for o in market.get("outcomes", []):

                            if o["name"] == "Over" and o["point"] == 2.5:
                                over25 = o["price"]

                            if o["name"] == "Under" and o["point"] == 2.5:
                                under25 = o["price"]

                    if market.get("key") == "btts":

                        for o in market.get("outcomes", []):

                            if o["name"] == "Yes":
                                goal = o["price"]

                            if o["name"] == "No":
                                nogoal = o["price"]

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
