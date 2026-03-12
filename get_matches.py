import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "next": 20
}

r = requests.get(url, headers=headers, params=params)

print("HTTP STATUS:", r.status_code)

data = r.json()

print("RISPOSTA API COMPLETA:")
print(json.dumps(data, indent=2))

with open("debug_api.json","w") as f:
    json.dump(data,f,indent=2)