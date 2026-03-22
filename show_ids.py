import json

# Carica matches
with open("data/matches_today.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

print("\n🔥 LISTA PARTITE CON ID 🔥\n")

for m in matches:
    fixture_id = m.get("fixture_id")
    home = m.get("home")
    away = m.get("away")
    date = m.get("date")
    time = m.get("time")

    print(f"{fixture_id} → {home} vs {away} | {date} {time}")

print("\n✅ Copia gli ID che ti servono in quotes_manual.json\n")