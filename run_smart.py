import os
from datetime import datetime

hour = datetime.utcnow().hour

# Italia UTC+1
italy_hour = (hour + 1) % 24

print(f"Ora Italia: {italy_hour}")

# SOLO 2 RUN
if italy_hour not in [10, 16]:
    print("⛔ Skip per risparmio API")
    exit()

print("🚀 RUN ATTIVO")

os.system("python get_matches.py")
os.system("python multigol_engine.py")