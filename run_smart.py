import os
from datetime import datetime

# Ora UTC
hour = datetime.utcnow().hour

print(f"Ora UTC: {hour}")

# 🇮🇹 Italia = UTC +2 (ora legale)
italy_hour = (hour + 2) % 24

print(f"Ora Italia: {italy_hour}")

# 🔥 SOLO 2 RUN AL GIORNO
if italy_hour not in [10, 16]:
    print("⛔ Skip per risparmio API")
    exit()

print("🚀 RUN ATTIVO")

# 🔽 ESECUZIONE SCRIPT
os.system("python get_matches.py")
os.system("python multigol_engine.py")

print("✅ Fine run")