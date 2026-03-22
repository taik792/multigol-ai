import os
import json
from datetime import datetime

# ===============================
# CHECK FILE ESISTENTE
# ===============================

MATCHES_FILE = "data/matches_today.json"

def is_file_valid():
    if not os.path.exists(MATCHES_FILE):
        return False

    with open(MATCHES_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except:
            return False

    # Se vuoto → rifai fetch
    if not data:
        return False

    return True

# ===============================
# MAIN
# ===============================

print("🔍 Controllo matches...")

if not is_file_valid():
    print("⚡ Nessun match valido → chiamo API")
    os.system("python get_matches.py")
else:
    print("✅ Matches già presenti → salto API")

print("⚙️ Avvio engine...")
os.system("python multigol_engine.py")

print("✅ Fine processo")