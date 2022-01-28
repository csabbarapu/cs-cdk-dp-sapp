from flask import Flask, request, jsonify
from math import factorial
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Creating flask api with factorial logic
@app.route("/api/v1/factorial", methods=["GET"])
def return_factorial():
    logging.info(request)
    if "number" in request.args:
        try:
            logging.info(f'Calculating factorial for {request.args["number"]}')
            number = int(request.args["number"])
            answer = {"factorial": factorial(number)}
            logging.info(f'Factorial for {request.args["number"]} is {answer}')
            return jsonify(answer)
        except ValueError:
            logging.error(f'Invalid value for number: {request.args["number"]}')
            return "Invalid value", 400
    logging.error(f"No number parameter provided")
    return "Please supply number parameter", 400


@app.route("/status", methods=["GET"])
def return_status():
    return "UP", 200
