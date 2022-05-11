from operator import itemgetter

from flask import Flask, jsonify, request
from .random_forest import random_forest

app = Flask(__name__)

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
        number_of_rounds=number_of_rounds
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
    return jsonify(prediction=result, input=input)