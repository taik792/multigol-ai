import os
import json

MATCHES_FILE = "data/matches_today.json"

def is_file_valid():
    if not os.path.exists(MATCHES_FILE):
        return False

    with open(MATCHES_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except:
            return False

    if not data:
        return False

    return True

print("🔍 Controllo matches...")

if not is_file_valid():
    print("⚡ File vuoto → chiamo API")
    os.system("python get_matches.py")
else:
    print("✅ Uso matches già salvati")

print("⚙️ Avvio engine...")
os.system("python multigol_engine.py")

print("✅ Fine processo")