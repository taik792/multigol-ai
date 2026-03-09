import requests
import json
import os
from datetime import datetime

# INSERISCI QUI LA TUA API KEY
API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")

# cartella dati
os.makedirs("data", exist_ok=True)

file_path = f"data/matches_{today}.json"

# controlla se esiste già il file di oggi
if os.path.exists(file_path):

    print("File partite già esistente. Nessuna chiamata API.")
    
    with open(file_path) as f:
        matches = json.load(f)

else:

    print("Scarico partite da API-Football...")

    params = {
        "date": today,
        "status": "NS"
    }

    response = requests.get(url, headers=headers, params=params)

    print("Status:", response.status_code)

    if response.status_code != 200:
        print("Errore API")
        print(response.text)
        exit()

    data = response.json()

    matches = []

    for m in data.get("response", []):

        matches.append({
            "home": m["teams"]["home"]["name"],
            "away": m["teams"]["away"]["name"],
            "league": m["league"]["name"]
        })

    matches = matches[:10]

    with open(file_path, "w") as f:
        json.dump(matches, f, indent=4)

    print("Partite salvate:", len(matches))

# mostra partite
for m in matches:
    print(m["home"], "vs", m["away"], "-", m["league"])
