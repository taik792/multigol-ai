import datetime
import subprocess

now = datetime.datetime.utcnow()
hour = now.hour

print(f"Ora UTC: {hour}")

# ✅ AUTOMATICO ORARI
if hour in [8, 14]:
    print("RUN AUTOMATICO")
    
    subprocess.run(["python", "get_matches.py"])
    subprocess.run(["python", "update_team_stats.py"])
    subprocess.run(["python", "multigol_engine.py"])

# ✅ MANUALE SEMPRE ATTIVO
else:
    print("RUN MANUALE (fallback)")
    
    subprocess.run(["python", "get_matches.py"])
    subprocess.run(["python", "update_team_stats.py"])
    subprocess.run(["python", "multigol_engine.py"])