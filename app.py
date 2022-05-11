from operator import itemgetter
from typing import Literal

import pandas as pd
from flask import Flask, jsonify, request
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def pretrain_model():
    """
    Pretrain model, usually used at the startup of the application, in order to
    prevent lag when accessing the prediction endpoint. Returns the trained Random Forest
    Classifier instance, the dataset, and the accuracy of the model.
    """
    data = pd.read_excel("./data/clean_ufc_data.xlsx", engine="openpyxl")
    features = data[
        [
            "R_odds",
            "B_odds",
            "better_rank",
            "no_of_rounds",
            "B_age",
            "B_current_lose_streak",
            "B_current_win_streak",
            "B_avg_SIG_STR_landed",
            "B_avg_SIG_STR_pct",
            "B_avg_SUB_ATT",
            "B_avg_TD_landed",
            "B_avg_TD_pct",
            "B_longest_win_streak",
            "B_losses",
            "B_total_rounds_fought",
            "B_total_title_bouts",
            "B_win_by_Decision_Majority",
            "B_win_by_Decision_Split",
            "B_win_by_Decision_Unanimous",
            "B_win_by_KO/TKO",
            "B_win_by_Submission",
            "B_win_by_TKO_Doctor_Stoppage",
            "B_wins",
            "B_Stance",
            "B_Height_cms",
            "B_Reach_cms",
            "B_Weight_lbs",
            "R_age",
            "R_current_lose_streak",
            "R_current_win_streak",
            "R_avg_SIG_STR_landed",
            "R_avg_SIG_STR_pct",
            "R_avg_SUB_ATT",
            "R_avg_TD_landed",
            "R_avg_TD_pct",
            "R_longest_win_streak",
            "R_losses",
            "R_total_rounds_fought",
            "R_total_title_bouts",
            "R_win_by_Decision_Majority",
            "R_win_by_Decision_Split",
            "R_win_by_Decision_Unanimous",
            "R_win_by_KO/TKO",
            "R_win_by_Submission",
            "R_win_by_TKO_Doctor_Stoppage",
            "R_wins",
            "R_Stance",
            "R_Height_cms",
            "R_Reach_cms",
            "R_Weight_lbs",
        ]
    ]
    label = data["Winner"]

    # train, test, and split
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.2)

    # random forest
    rf = RandomForestClassifier(random_state=42)
    rf.fit(x_train, y_train)
    y_pred_rf = rf.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_pred_rf)

    # return random forest, data, and accuracy
    return rf, data, accuracy


def random_forest(
    red_fighter: str,
    blue_fighter: str,
    red_odds: int,
    blue_odds: int,
    better_rank: Literal["0", "1", "2"],
    number_of_rounds: Literal["3", "5"],
    rf: RandomForestClassifier,
    data: pd.DataFrame,
):
    """
    This function will perform data prediction based on the Google Colab script.
    """
    # create holder for information
    fightInfo = []
    statsFighterRed = []
    statsFighterBlue = []

    # fight info
    fightInfo.append(red_odds)
    fightInfo.append(blue_odds)
    fightInfo.append(number_of_rounds)
    fightInfo.append(better_rank)

    # for loop to iterate throughout rows
    for i, j in data.iterrows():
        if red_fighter == j[1]:
            for m in range(34, 57):
                statsFighterRed.append(j[m])
            break

        elif red_fighter == j[2]:
            for n in range(11, 34):
                statsFighterRed.append(j[n])
            break

        else:
            continue

    # same as above
    for i, j in data.iterrows():
        if blue_fighter == j[1]:
            for m in range(34, 57):
                statsFighterBlue.append(j[m])
            break

        elif blue_fighter == j[2]:
            for n in range(11, 34):
                statsFighterBlue.append(j[n])

            break
        else:
            continue

    fightInfo.extend(statsFighterBlue)
    fightInfo.extend(statsFighterRed)

    fight_pred = rf.predict([fightInfo])

    return fight_pred[0]


# initial bootstrap, define app, pretrain model, and reuse the RF instance as global variable
def create_app():
    print(" * (RF) Training model, please wait before the app can start...")
    rf, data, accuracy = pretrain_model()

    # define app
    print(" * (RF) Model has been successfully pretrained. Starting app...")
    app = Flask(__name__)

    # with app context, do...
    with app.app_context():

        @app.route("/")
        def hello():
            return jsonify(status="success", message="Hello, World!")

        # Expected request body:
        # {
        #     "redFighter": "Dustin Poirier",
        #     "blueFighter": "Tony Ferguson",
        #     "redOdds": 120,
        #     "blueOdds": -120,
        #     "betterRank": 0,
        #     "numberOfRounds": 5
        # }
        @app.route("/predict", methods=["POST"])
        def predict():
            # fetch from request body
            (
                red_fighter,
                blue_fighter,
                red_odds,
                blue_odds,
                better_rank,
                number_of_rounds,
            ) = itemgetter(
                "redFighter",
                "blueFighter",
                "redOdds",
                "blueOdds",
                "betterRank",
                "numberOfRounds",
            )(
                request.json
            )

            # make prediction based on the trained model
            result = random_forest(
                red_fighter=red_fighter,
                blue_fighter=blue_fighter,
                red_odds=red_odds,
                blue_odds=blue_odds,
                better_rank=better_rank,
                number_of_rounds=number_of_rounds,
                rf=rf,
                data=data,
            )

            # encapsulate input in nested json
            input = {
                "redFighter": red_fighter,
                "blueFighter": blue_fighter,
                "redOdds": red_odds,
                "blueOdds": blue_odds,
                "betterRank": better_rank,
                "numberOfRounds": number_of_rounds,
            }

            # return data as json, this will be read by the android app
            return jsonify(prediction=result, input=input, accuracy=accuracy)

    # return app instance
    return app


# in startup, start the 'create_app' function
if __name__ == "__main__":
    create_app()
