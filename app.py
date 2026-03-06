import streamlit as st
from odds_api_scraper import get_matches
from multigol_engine import analyze_matches

st.set_page_config(page_title="Multigol AI Scanner", layout="wide")

st.title("⚽ MULTIGOL AI SCANNER")

matches = get_matches()

st.write("Partite analizzate:", len(matches))

if not matches:
    st.warning("Nessuna partita trovata")
    st.stop()

results = analyze_matches(matches)

# TOP SICURE
st.header("🔥 TOP SICURE")

for r in results["top"]:

    st.subheader(f"{r['home']} vs {r['away']}")

    st.write("Over 2.5:", r["over25"])

    st.write("Multigol Casa:", r["multigol_home"])
    st.write("Multigol Ospite:", r["multigol_away"])

    st.write("Quota stimata:", r["odds"])

    st.write("Score AI:", r["score"])

    st.markdown("---")


# PARTITE GIOCABILI
st.header("⚽ PARTITE GIOCABILI")

for r in results["playable"]:

    st.subheader(f"{r['home']} vs {r['away']}")

    st.write("Over 2.5:", r["over25"])

    st.write("Multigol Casa:", r["multigol_home"])
    st.write("Multigol Ospite:", r["multigol_away"])

    st.write("Quota stimata:", r["odds"])

    st.write("Score AI:", r["score"])

    st.markdown("---")


# BOLLETTE
st.header("🔥 BOLLETTE CONSIGLIATE")

if not results["bets"]:
    st.write("Nessuna bolletta trovata")

for b in results["bets"]:

    st.subheader("Bolletta")

    st.write(b["match1"])
    st.write("Multigol Casa:", b["mg1_home"])
    st.write("Multigol Ospite:", b["mg1_away"])

    st.write("")

    st.write(b["match2"])
    st.write("Multigol Casa:", b["mg2_home"])
    st.write("Multigol Ospite:", b["mg2_away"])

    st.write("Quota totale stimata:", b["quota"])

    st.markdown("---")
