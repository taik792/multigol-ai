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

            match_time = datetime.fromisoformat(commence.replace("Z","+00:00"))

            # scarta partite finite da troppo
            if match_time < now - timedelta(hours=2):
                continue

            home = game.get("home_team")
            away = game.get("away_team")

            over25 = None
            goal = None

            for bookmaker in game.get("bookmakers",[]):

                for market in bookmaker.get("markets",[]):

                    if market.get("key") == "totals":

                        for outcome in market.get("outcomes",[]):

                            if outcome.get("name") == "Over" and outcome.get("point") == 2.5:
                                over25 = outcome.get("price")

                    if market.get("key") == "btts":

                        for outcome in market.get("outcomes",[]):

                            if outcome.get("name") == "Yes":
                                goal = outcome.get("price")

            if over25:

                matches.append({
                    "home": home,
                    "away": away,
                    "over25": over25,
                    "goal": goal if goal else 1.90
                })


    return matches
