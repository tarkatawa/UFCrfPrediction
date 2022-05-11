from operator import itemgetter

from flask import Flask, jsonify, request
from .random_forest import pretrain_model, random_forest

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
            red_fighter, blue_fighter, red_odds, blue_odds, better_rank, number_of_rounds = itemgetter("redFighter", "blueFighter", "redOdds", "blueOdds", "betterRank", "numberOfRounds")(request.json)
            
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
                'redFighter': red_fighter,
                'blueFighter': blue_fighter,
                'redOdds': red_odds,
                'blueOdds': blue_odds,
                'betterRank': better_rank,
                'numberOfRounds': number_of_rounds,
            }

            # return data as json, this will be read by the android app
            return jsonify(prediction=result, input=input, accuracy=accuracy)

    # return app instance
    return app

# in startup, start the 'create_app' function
if __name__ =="__main__":
    create_app()