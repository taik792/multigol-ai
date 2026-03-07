import requests
import json

API_KEY = "b90932e65c14be06a870fd50fcd20ddc"

# carichiamo le partite trovate
with open("data/matches_today.json") as f:
    matches = json.load(f)

url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?regions=eu&markets=totals&apiKey={API_KEY}"

response = requests.get(url)
data = response.json()

odds = {}

for match in data:

    home = match["home_team"]
    away = match["away_team"]

    key = f"{home} vs {away}"

    try:

        bookmakers = match["bookmakers"][0]
        markets = bookmakers["markets"][0]
        outcomes = markets["outcomes"]

        # prendiamo la quota più vicina al multigol
        price = outcomes[0]["price"]

        odds[key] = {
            "multigol_2_4": price
        }

    except:
        pass


with open("quotes/odds.json", "w") as f:
    json.dump(odds, f, indent=4)

print("Odds reali salvate:", len(odds))
