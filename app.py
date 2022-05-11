from operator import itemgetter

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify(status="success", message="Hello, World!")

# Schema:
# {
#     "redFighter": "Nicholas Dwiarto",
#     "blueFighter": "Random Blue Fighter",
#     "redOdds": 100,
#     "blueOdds": -120,
#     "betterRank": 0,
#     "numberOfRounds": 3
# }
@app.route("/predict", methods=["POST"])
def predict():
    # fetch from request body
    redFighter, blueFighter, redOdds, blueOdds, betterRank, numberOfRounds = itemgetter("redFighter", "blueFighter", "redOdds", "blueOdds", "betterRank", "numberOfRounds")(request.json)
    
    # make prediction based on the trained model
    # ...

    # return data as json, this will be read by the android app
    return jsonify(redFighter, blueFighter, redOdds, blueOdds, betterRank, numberOfRounds)