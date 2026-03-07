import json
import os


def load_matches():

    with open("data/matches_today.json", "r") as f:
        return json.load(f)


def load_odds():

    with open("quotes/odds.json", "r") as f:
        return json.load(f)


def calculate_expected_goals(home_avg, away_avg, home_con, away_con):

    return (home_avg + away_avg + home_con + away_con) / 2


def multigol_range(xg):

    if xg < 1.5:
        return "0-2"

    elif xg < 2.5:
        return "1-3"

    elif xg < 3.5:
        return "2-4"

    else:
        return "2-5"


def confidence_score(xg):

    score = (xg / 4) * 100

    if score > 100:
        score = 100

    return round(score, 1)


def run_engine():

    matches = load_matches()
    odds = load_odds()

    predictions = []

    for m in matches:

        home = m["home"]
        away = m["away"]

        home_avg = m["home_goals_avg"]
        away_avg = m["away_goals_avg"]

        home_con = m["home_conceded"]
        away_con = m["away_conceded"]

        xg = calculate_expected_goals(
            home_avg,
            away_avg,
            home_con,
            away_con
        )

        multigol = multigol_range(xg)

        confidence = confidence_score(xg)

        match_key = f"{home}-{away}"

        q = odds.get(match_key, {})

        prediction = {

            "match": match_key,

            "expected_goals": round(xg,2),

            "multigol": multigol,

            "confidence": confidence,

            "odds":{

                "1": q.get("1"),
                "X": q.get("X"),
                "2": q.get("2"),

                "over25": q.get("over25"),
                "under25": q.get("under25"),

                "btts_yes": q.get("btts_yes"),
                "btts_no": q.get("btts_no")

            }

        }

        predictions.append(prediction)

    os.makedirs("output", exist_ok=True)

    with open("output/multigol_predictions.json","w") as f:
        json.dump(predictions, f, indent=4)

    print("Multigol Engine completato")


if __name__ == "__main__":
    run_engine()
