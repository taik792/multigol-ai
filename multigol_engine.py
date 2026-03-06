def calculate_score(match):

    score = 0

    over25 = match["over25"]
    under25 = match["under25"]

    # partita molto aperta
    if over25 <= 1.65 and under25 >= 2.10:
        score += 60

    # buona probabilità di gol
    elif over25 <= 1.75 and under25 >= 2.00:
        score += 45

    # partita media
    elif over25 <= 1.90:
        score += 30

    # partita incerta
    else:
        score += 10

    return score


def generate_multigol(over25):

    # partita molto aperta
    if over25 <= 1.65:

        return {
            "home": "1-4",
            "away": "1-3"
        }

    # partita con gol probabili
    elif over25 <= 1.80:

        return {
            "home": "1-3",
            "away": "1-2"
        }

    # partita equilibrata
    elif over25 <= 2.00:

        return {
            "home": "0-3",
            "away": "0-2"
        }

    # partita chiusa
    else:

        return {
            "home": "0-2",
            "away": "0-1"
        }


def estimate_odds(match):

    over25 = match["over25"]

    if over25 <= 1.65:
        return 1.55
    elif over25 <= 1.80:
        return 1.60
    elif over25 <= 2.00:
        return 1.65
    else:
        return 1.70


def create_bets(matches):

    bets = []

    for i in range(len(matches)):
        for j in range(i + 1, len(matches)):

            m1 = matches[i]
            m2 = matches[j]

            quota = m1["odds"] * m2["odds"]

            # quota totale circa 3
            if 2.8 <= quota <= 3.4:

                bets.append({

                    "match1": m1["home"] + " vs " + m1["away"],
                    "mg1_home": m1["multigol_home"],
                    "mg1_away": m1["multigol_away"],

                    "match2": m2["home"] + " vs " + m2["away"],
                    "mg2_home": m2["multigol_home"],
                    "mg2_away": m2["multigol_away"],

                    "quota": round(quota, 2)

                })

    return bets[:5]


def analyze_matches(matches):

    results = []

    for match in matches:

        score = calculate_score(match)

        multigol = generate_multigol(match["over25"])

        odds = estimate_odds(match)

        results.append({

            "home": match["home"],
            "away": match["away"],

            "score": score,

            "over25": match["over25"],
            "under25": match["under25"],

            "multigol_home": multigol["home"],
            "multigol_away": multigol["away"],

            "odds": odds

        })

    # ordina per score migliore
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    top_matches = results[:6]

    playable_matches = results[6:]

    bets = create_bets(results)

    return {
        "top": top_matches,
        "playable": playable_matches,
        "bets": bets
    }
