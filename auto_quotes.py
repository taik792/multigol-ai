import json

# Carica matches
with open("data/matches_today.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

quotes = []

# quante partite vuoi preparare
NUM_MATCHES = 5

for m in matches[:NUM_MATCHES]:
    quotes.append({
        "fixture_id": m.get("fixture_id"),

        "q1": 0,
        "qx": 0,
        "q2": 0,

        "qgg": 0,
        "qng": 0,

        "c_o05": 0,
        "c_o15": 0,

        "o_o05": 0,
        "o_o15": 0
    })

# salva file
with open("data/quotes_manual.json", "w", encoding="utf-8") as f:
    json.dump(quotes, f, indent=2)

print(f"✅ Creato quotes_manual.json con {NUM_MATCHES} partite")