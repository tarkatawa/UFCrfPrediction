from operator import itemgetter

from flask import Flask, jsonify, request

app = Flask(__name__)

def random_forest():
    """
    This function will perform data prediction based on the Google Colab script.
    """
    return True

@app.route("/")
def hello():
    return jsonify(status="success", message="Hello, World!")

# Schema:
# {
#     "redFighter": "Random Red Fighter",
#     "blueFighter": "Random Blue Fighter",
#     "redOdds": 100,
#     "blueOdds": -120,
#     "betterRank": 0,
#     "numberOfRounds": 3
# }
@app.route("/predict", methods=["POST"])
def predict():
    # fetch from request body
    red_fighter, blue_fighter, red_odds, blue_odds, better_rank, number_of_rounds = itemgetter("redFighter", "blueFighter", "redOdds", "blueOdds", "betterRank", "numberOfRounds")(request.json)
    
    # make prediction based on the trained model
    result = random_forest()

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