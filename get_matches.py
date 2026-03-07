import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures?next=20"

headers = {
"x-apisports-key": API_KEY
}

response = requests.get(url, headers=headers)
data = response.json()

print("API response:", data)

if "response" not in data:
print("Errore API")
exit()

matches = []

for game in data["response"]:

```
home = game["teams"]["home"]["name"]
away = game["teams"]["away"]["name"]

matches.append({
    "home": home,
    "away": away
})
```

with open("data/matches_today.json", "w") as f:
json.dump(matches, f, indent=4)

print("Matches salvati")
