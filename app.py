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
        #     "nameFighter": "Brandon Moreno"
        #     "weightClass": "Flyweight"
        # }
        @app.route("/weightclass", methods=["POST"])
        def weightclass():
            # fetch from request body
            (
                name_fighter,
                weight_chosen
            ) = itemgetter(
                "nameFighter",
                "weightChosen"

            )(
                request.json
            )

            # Get fighter names to face
            # Mens
            flyweights = []
            bantamweights = []
            featherweights = []
            lightweights = []
            welterweights = []
            middleweights = []
            lightheavyweights = []
            heavyweights = []

            # Womens
            wmstrawweights = []
            wmflyweights = []
            wmbantamweights = []
            wmfeatherweights = []

            for _, j in data.iterrows():
                if(j[6] == "Flyweight"):
                    flyweights.append(j[1])
                    flyweights.append(j[2])
                elif(j[6] == "Bantamweight"):
                    bantamweights.append(j[1])
                    bantamweights.append(j[2])
                elif(j[6] == "Featherweight"):
                    featherweights.append(j[1])
                    featherweights.append(j[2])
                elif(j[6] == "Lightweight"):
                    lightweights.append(j[1])
                    lightweights.append(j[2])
                elif(j[6] == "Welterweight"):
                    welterweights.append(j[1])
                    welterweights.append(j[2])
                elif(j[6] == "Middleweight"):
                    middleweights.append(j[1])
                    middleweights.append(j[2])
                elif(j[6] == "Light Heavyweight"):
                    lightheavyweights.append(j[1])
                    lightheavyweights.append(j[2])
                elif(j[6] == "Heavyweight"):
                    heavyweights.append(j[1])
                    heavyweights.append(j[2])
                elif(j[6] == "Women's Strawweight"):
                    wmstrawweights.append(j[1])
                    wmstrawweights.append(j[2])
                elif(j[6] == "Women's Flyweight"):
                    wmflyweights.append(j[1])
                    wmflyweights.append(j[2])
                elif(j[6] == "Women's Bantamweight"):
                    wmbantamweights.append(j[1])
                    wmbantamweights.append(j[2])
                elif(j[6] == "Women's Featherweight"):
                    wmfeatherweights.append(j[1])
                    wmfeatherweights.append(j[2])  
                else:
                    continue

            flyweights = list(dict.fromkeys(flyweights))
            bantamweights = list(dict.fromkeys(bantamweights))
            featherweights = list(dict.fromkeys(featherweights))
            lightweights = list(dict.fromkeys(lightweights))
            welterweights = list(dict.fromkeys(welterweights))
            middleweights = list(dict.fromkeys(middleweights))
            lightheavyweights = list(dict.fromkeys(lightheavyweights))
            heavyweights = list(dict.fromkeys(heavyweights))
            wmstrawweights = list(dict.fromkeys(wmstrawweights))
            wmflyweights = list(dict.fromkeys(wmflyweights))
            wmbantamweights = list(dict.fromkeys(wmbantamweights))
            wmfeatherweights = list(dict.fromkeys(wmfeatherweights))

            flyweightsResult = []
            bantamweightsResult = []
            featherweightsResult = []
            lightweightsResult = []
            welterweightsResult = []
            middleweightsResult = []
            lightheavyweightsResult = []
            heavyweightsResult = []

            wmstrawweightResult = []
            wmflyweightsResult = []
            wmbantamweightsResult = []
            wmfeatherweightsResult = []       

            fightInfo = [-110, -110, 3, 2]
            statsFighter = []

            # find stats of inputted fighter
            for _, j in data.iterrows():
                if(name_fighter == j[1]):
                    fighterGender = j[7]
                    for m in range(34, 57):
                        statsFighter.append(j[m])
                    fightInfo.extend(statsFighter)
                    break
                elif(name_fighter == j[2]):
                    fighterGender = j[7]
                    for n in range(11, 34):
                        statsFighter.append(j[n])
                    fightInfo.extend(statsFighter)
                    break
                else:
                    continue

            temp = fightInfo            
            if (name_fighter in flyweights):
                flyweights.remove(name_fighter)
            if (name_fighter in bantamweights):
                bantamweights.remove(name_fighter)
            if (name_fighter in featherweights):
                featherweights.remove(name_fighter)
            if (name_fighter in lightweights):
                lightweights.remove(name_fighter)
            if (name_fighter in welterweights):
                welterweights.remove(name_fighter)
            if (name_fighter in middleweights):
                middleweights.remove(name_fighter)
            if (name_fighter in lightheavyweights):  
                lightheavyweights.remove(name_fighter)
            if (name_fighter in heavyweights):
                heavyweights.remove(name_fighter)
            if (name_fighter in wmstrawweights):
                wmstrawweights.remove(name_fighter)
            if (name_fighter in wmflyweights):  
                wmflyweights.remove(name_fighter)
            if (name_fighter in wmbantamweights):  
                wmbantamweights.remove(name_fighter)
            if (name_fighter in wmfeatherweights):  
                wmfeatherweights.remove(name_fighter)
            
            if weight_chosen == "Flyweight":
            # predict inputted fighter vs all flyweights
                if fighterGender == "MALE":
                    for fighter in flyweights:
                        for _, j in data.iterrows():
                            if(fighter == j[1]):
                                for m in range(34, 57):
                                    temp.append(j[m])
                                break
                            elif(fighter == j[2]):
                                for n in range(11, 34):
                                    temp.append(j[n])
                                break
                            else:
                                continue
                        #Predict
                        fight_pred = rf.predict([temp])

                        #Input to results
                        flyweightsResult.append(fight_pred[0])

                        #Set temp back to default
                        temp.clear()
                        temp = [-110, -110, 3, 2]
                        temp.extend(statsFighter)

                    #count percentage
                    flyweightPct = flyweightsResult.count('Red') / len(flyweightsResult)
                    print(flyweightPct)
                return jsonify(flyweightPct = flyweightPct)  
                
            if weight_chosen == "Bantamweight":
            # predict inputted fighter vs all flyweights
                if fighterGender == "MALE":
                    for fighter in bantamweights:
                        for _, j in data.iterrows():
                            if(fighter == j[1]):
                                for m in range(34, 57):
                                    temp.append(j[m])
                                break
                            elif(fighter == j[2]):
                                for n in range(11, 34):
                                    temp.append(j[n])
                                break
                            else:
                                continue
                        #Predict
                        fight_pred = rf.predict([temp])

                        #Input to results
                        bantamweightsResult.append(fight_pred[0])

                        #Set temp back to default
                        temp.clear()
                        temp = [-110, -110, 3, 2]
                        temp.extend(statsFighter)

                    #count percentage
                    bantamweightPct = bantamweightsResult.count('Red') / len(bantamweightsResult)
                    print(bantamweightPct)                

                return jsonify(flyweightPct = bantamweightPct)         

            # Featherweight
            if weight_chosen == "Featherweight":
            # predict inputted fighter vs all bantamweights
                if fighterGender == "MALE":
                    for fighter in featherweights:
                        for _, j in data.iterrows():
                            if(fighter == j[1]):
                                for m in range(34, 57):
                                    temp.append(j[m])
                                break
                            elif(fighter == j[2]):
                                for n in range(11, 34):
                                    temp.append(j[n])
                                break
                            else:
                                continue
                        #Predict
                        fight_pred = rf.predict([temp])

                        #Input to results
                        featherweightsResult.append(fight_pred[0])

                        #Set temp back to default
                        temp.clear()
                        temp = [-110, -110, 3, 2]
                        temp.extend(statsFighter)

                    #count percentage
                    featherweightPct = featherweightsResult.count('Red') / len(featherweightsResult)
                    print(featherweightPct)
                return jsonify(flyweightPct = featherweightPct)

            # Lightweight
            if weight_chosen == "Lightweight":
            # predict inputted fighter vs all featherweights
                if fighterGender == "MALE":
                    for fighter in lightweights:
                        for _, j in data.iterrows():
                            if(fighter == j[1]):
                                for m in range(34, 57):
                                    temp.append(j[m])
                                break
                            elif(fighter == j[2]):
                                for n in range(11, 34):
                                    temp.append(j[n])
                                break
                            else:
                                continue
                        #Predict
                        fight_pred = rf.predict([temp])

                        #Input to results
                        lightweightsResult.append(fight_pred[0])

                        #Set temp back to default
                        temp.clear()
                        temp = [-110, -110, 3, 2]
                        temp.extend(statsFighter)

                    #count percentage
                    lightweightPct = lightweightsResult.count('Red') / len(lightweightsResult)
                    print(lightweightPct)
                return jsonify(flyweightPct = lightweightPct)

            # Welterweight
            if weight_chosen == "Welterweight":
            # predict inputted fighter vs all featherweights
                if fighterGender == "MALE":
                    for fighter in welterweights:
                        for _, j in data.iterrows():
                            if(fighter == j[1]):
                                for m in range(34, 57):
                                    temp.append(j[m])
                                break
                            elif(fighter == j[2]):
                                for n in range(11, 34):
                                    temp.append(j[n])
                                break
                            else:
                                continue
                        #Predict
                        fight_pred = rf.predict([temp])

                        #Input to results
                        welterweightsResult.append(fight_pred[0])

                        #Set temp back to default
                        temp.clear()
                        temp = [-110, -110, 3, 2]
                        temp.extend(statsFighter)

                    #count percentage
                    welterweightPct = welterweightsResult.count('Red') / len(welterweightsResult)
                    print(welterweightPct)
                return jsonify(flyweightPct = welterweightPct)            

            # Middleweight
            if weight_chosen == "Middleweight":
            # predict inputted fighter vs all featherweights
                if fighterGender == "MALE":
                    for fighter in middleweights:
                        for _, j in data.iterrows():
                            if(fighter == j[1]):
                                for m in range(34, 57):
                                    temp.append(j[m])
                                break
                            elif(fighter == j[2]):
                                for n in range(11, 34):
                                    temp.append(j[n])
                                break
                            else:
                                continue
                        #Predict
                        fight_pred = rf.predict([temp])

                        #Input to results
                        middleweightsResult.append(fight_pred[0])

                        #Set temp back to default
                        temp.clear()
                        temp = [-110, -110, 3, 2]
                        temp.extend(statsFighter)

                    #count percentage
                    middleweightPct = middleweightsResult.count('Red') / len(middleweightsResult)
                    print(middleweightPct)
                return jsonify(flyweightPct = middleweightPct)  

            # Light Heavyweight
            if weight_chosen == "Lightheavyweight":
            # predict inputted fighter vs all featherweights
                if fighterGender == "MALE":
                    for fighter in lightheavyweights:
                        for _, j in data.iterrows():
                            if(fighter == j[1]):
                                for m in range(34, 57):
                                    temp.append(j[m])
                                break
                            elif(fighter == j[2]):
                                for n in range(11, 34):
                                    temp.append(j[n])
                                break
                            else:
                                continue
                        #Predict
                        fight_pred = rf.predict([temp])

                        #Input to results
                        lightheavyweightsResult.append(fight_pred[0])

                        #Set temp back to default
                        temp.clear()
                        temp = [-110, -110, 3, 2]
                        temp.extend(statsFighter)

                    #count percentage
                    lightheavyweightPct = lightheavyweightsResult.count('Red') / len(lightheavyweightsResult)
                    print(lightheavyweightPct)
                return jsonify(flyweightPct = lightheavyweightPct)  

            # Heavyweight
            if weight_chosen == "Heavyweight":
            # predict inputted fighter vs all featherweights
                if fighterGender == "MALE":
                    for fighter in heavyweights:
                        for _, j in data.iterrows():
                            if(fighter == j[1]):
                                for m in range(34, 57):
                                    temp.append(j[m])
                                break
                            elif(fighter == j[2]):
                                for n in range(11, 34):
                                    temp.append(j[n])
                                break
                            else:
                                continue
                        #Predict
                        fight_pred = rf.predict([temp])

                        #Input to results
                        heavyweightsResult.append(fight_pred[0])

                        #Set temp back to default
                        temp.clear()
                        temp = [-110, -110, 3, 2]
                        temp.extend(statsFighter)

                    #count percentage
                    heavyweightPct = heavyweightsResult.count('Red') / len(heavyweightsResult)
                    print(heavyweightPct)
                return jsonify(flyweightPct = heavyweightPct) 

            # wmStrawweight

            # wmFlyweight

            # wmBantamweight

            # wmFeatherweight



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

        # Expected request body:
        # {
        #     "genderFighter": "Male",
        #     "weightFighter": "Featherweight"
        # }
        @app.route("/fighters", methods=["POST"])
        def get_fighters():
            (
                gender_fighter,
                weight_fighter
            ) = itemgetter(
                "genderFighter",
                "weightFighter",
            )(
                request.json
            )

            # Logic to get fighters based on class
            list_fighters = set()
            if gender_fighter == "Male":
                if weight_fighter == "Flyweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Flyweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Bantamweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Bantamweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Featherweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Featherweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Lightweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Lightweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Welterweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Welterweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Middleweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Middleweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Light Heavyweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Light Heavyweight":
                            list_fighters.add(row['R_fighter'])

                else:
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Heavyweight":
                            list_fighters.add(row['R_fighter'])

            else:
                if weight_fighter == "Strawweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Women's Strawweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Flyweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Women's Flyweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Bantamweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Women's Bantamweight":
                            list_fighters.add(row['R_fighter'])

                else:
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Women's Featherweight":
                            list_fighters.add(row['R_fighter'])
            
            return jsonify(list_fighters=list(list_fighters))
        
        @app.route("/fighters2", methods=["POST"])
        def get_fighters_dua():
            (
                gender_fighter,
                weight_fighter
            ) = itemgetter(
                "genderFighter",
                "weightFighter",
            )(
                request.json
            )

            # Logic to get fighters based on class
            list_fighters = set()
            if gender_fighter == "Male":
                if weight_fighter == "Flyweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Flyweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Bantamweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Bantamweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Featherweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Featherweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Lightweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Lightweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Welterweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Welterweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Middleweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Middleweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Light Heavyweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Light Heavyweight":
                            list_fighters.add(row['R_fighter'])

                else:
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Heavyweight":
                            list_fighters.add(row['R_fighter'])

            else:
                if weight_fighter == "Strawweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Women's Strawweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Flyweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Women's Flyweight":
                            list_fighters.add(row['R_fighter'])

                elif weight_fighter == "Bantamweight":
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Women's Bantamweight":
                            list_fighters.add(row['R_fighter'])

                else:
                    for _, row in data.iterrows():
                        if row["weight_class"] == "Women's Featherweight":
                            list_fighters.add(row['R_fighter'])
            
            return jsonify(list_fighters2=list(list_fighters))

    # return app instance
    return app


# in startup, start the 'create_app' function
if __name__ == "__main__":
    create_app()
