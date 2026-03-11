import json
import os

MATCHES_FILE = "data/matches_today.json"
STATS_FILE = "data/teams_stats.json"

# carica partite
with open(MATCHES_FILE) as f:
    matches = json.load(f)

stats = {}

for m in matches:

    home = m["home"]
    away = m["away"]

    if home not in stats:
        stats[home] = {
            "scored": 1.5,
            "conceded": 1.2
        }

    if away not in stats:
        stats[away] = {
            "scored": 1.3,
            "conceded": 1.4
        }

# salva statistiche
with open(STATS_FILE, "w") as f:
    json.dump(stats, f, indent=2)

print("Team stats updated")