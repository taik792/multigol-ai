def calculate_score(match):

    over = match["over25"]
    under = match["under25"]

    score = 0

    # partita molto aperta
    if over <= 1.55:
        score += 50

    # partita offensiva
    elif over <= 1.65:
        score += 40

    # partita normale
    elif over <= 1.80:
        score += 30

    # partita equilibrata
    elif over <= 2.00:
        score += 20

    else:
        score += 10

    return score


def generate_multigol(match):

    over = match["over25"]
    under = match["under25"]

    diff = abs(over - under)

    # partita con tanti gol
    if over <= 1.55:

        return {
            "home": "2-4",
            "away": "1-3"
        }

    # offensiva
    elif over <= 1.65:

        return {
            "home": "1-4",
            "away": "1-3"
        }

    # partita normale
    elif over <= 1.75:

        return {
            "home": "1-3",
            "away": "1-2"
        }

    # partita equilibrata
    elif over <= 1.90:

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

    over = match["over25"]

    if over <= 1.55:
        return 1.55
    elif over <= 1.65:
        return 1.60
    elif over <= 1.75:
        return 1.65
    elif over <= 1.90:
        return 1.70
    else:
        return 1.75


def create_bets(matches):

    bets = []

    for i in range(len(matches)):
        for j in range(i + 1, len(matches)):

            m1 = matches[i]
            m2 = matches[j]

            quota = m1["odds"] * m2["odds"]

            # quota target circa 3
            if 2.8 <= quota <= 3.4:

                bets.append({

                    "match1": f"{m1['home']} vs {m1['away']}",
                    "mg1_home": m1["multigol_home"],
                    "mg1_away": m1["multigol_away"],

                    "match2": f"{m2['home']} vs {m2['away']}",
                    "mg2_home": m2["multigol_home"],
                    "mg2_away": m2["multigol_away"],

                    "quota": round(quota, 2)

                })

    return bets[:5]


def analyze_matches(matches):

    results = []

    for match in matches:

        score = calculate_score(match)

        multigol = generate_multigol(match)

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

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    top_matches = results[:6]

    playable_matches = results[6:]

    bets = create_bets(results)

    return {
        "top": top_matches,
        "playable": playable_matches,
        "bets": bets
    }
