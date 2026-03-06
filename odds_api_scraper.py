import requests
import streamlit as st
from datetime import datetime, timezone, timedelta

API_KEY = st.secrets["ODDS_API_KEY"]

# molti più campionati
sports = [

    "soccer_epl",
    "soccer_italy_serie_a",
    "soccer_spain_la_liga",
    "soccer_germany_bundesliga",
    "soccer_france_ligue_one",

    "soccer_netherlands_eredivisie",
    "soccer_portugal_primeira_liga",
    "soccer_turkey_super_league",
    "soccer_belgium_first_div",
    "soccer_austria_bundesliga",

    "soccer_denmark_superliga",
    "soccer_sweden_allsvenskan",
    "soccer_brazil_campeonato",
    "soccer_argentina_primera_division"

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
            "markets": "totals",
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

            start = datetime.fromisoformat(commence.replace("Z", "+00:00"))

            # filtro oggi + domani
            if start < now or start > tomorrow:
                continue

            home = game.get("home_team")
            away = game.get("away_team")

            over25 = None
            under25 = None

            for bookmaker in game.get("bookmakers", []):

                for market in bookmaker.get("markets", []):

                    if market.get("key") == "totals":

                        for outcome in market.get("outcomes", []):

                            if outcome.get("name") == "Over" and outcome.get("point") == 2.5:
                                over25 = outcome.get("price")

                            if outcome.get("name") == "Under" and outcome.get("point") == 2.5:
                                under25 = outcome.get("price")

            if over25:

                matches.append({

                    "home": home,
                    "away": away,

                    "over25": over25,
                    "under25": under25 if under25 else 2.0,

                    "goal": 1.85,
                    "nogoal": 1.95

                })

    return matches
