import datetime
import subprocess

now = datetime.datetime.utcnow()
hour = now.hour

print(f"Ora UTC: {hour}")

# 08 UTC = 10 Italia
# 14 UTC = 16 Italia

if hour == 8:
    print("RUN COMPLETO (mattina)")
    subprocess.run(["python", "get_matches.py"])
    subprocess.run(["python", "update_team_stats.py"])
    subprocess.run(["python", "multigol_engine.py"])

elif hour == 14:
    print("RUN LEGGERO (pomeriggio)")
    subprocess.run(["python", "multigol_engine.py"])

else:
    print("Orario non previsto")