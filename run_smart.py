import os
import json
from datetime import datetime

MATCHES_FILE = "data/matches_today.json"

def is_today():
    if not os.path.exists(MATCHES_FILE):
        return False

    with open(MATCHES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        return False

    first_date = data[0].get("date", "")
    return datetime.today().strftime("%Y-%m-%d") in first_date

print("🔍 Controllo matches...")

if not is_today():
    print("⚡ API RUN (una volta al giorno)")
    os.system("python get_matches.py")
else:
    print("✅ Uso cache (NO API)")

print("⚙️ Engine...")
os.system("python multigol_engine.py")

print("✅ Fine")