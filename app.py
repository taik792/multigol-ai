import streamlit as st
from matches_scraper import get_matches
from multigol_engine import analyze_matches

st.title("⚽ MULTIGOL AI SCANNER")

matches = get_matches()

st.write("Partite analizzate:", len(matches))

results = analyze_matches(matches)

st.header("🔥 TOP SICURE")

for r in results["top"]:

    st.write(f"### {r['home']} vs {r['away']}")
    st.write("Over 2.5:", r["over25"])
    st.write("Goal:", r["goal"])
    st.write("Multigol Casa:", r["multigol_home"])
    st.write("Multigol Ospite:", r["multigol_away"])
    st.write("Score:", r["score"])
    st.write("---")

st.header("⚽ PARTITE GIOCABILI")

for r in results["playable"][:10]:

    st.write(f"{r['home']} vs {r['away']}")
    st.write("Multigol:", r["multigol_home"], "-", r["multigol_away"])
    st.write("---")

st.header("🔥 BOLLETTE CONSIGLIATE")

for b in results["bets"]:

    st.write("### Bolletta")

    st.write(b["match1"])
    st.write("Multigol:", b["mg1_home"], "-", b["mg1_away"])

    st.write(b["match2"])
    st.write("Multigol:", b["mg2_home"], "-", b["mg2_away"])

    st.write("Quota stimata:", b["quota"])
    st.write("---")