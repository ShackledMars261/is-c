from flask import Flask, request
import helpers
import random
import client
import json

cfg = helpers.importyaml()

app = Flask(__name__)

@app.route("/listener", methods=["POST"])
def listener():
    requestdata = request.get_json()
    print(requestdata)
    data = requestdata["data"]
    print(data)
    number = random_number(data["lowerBound"], data["upperBound"])
    print(number)
    responsedata = json.dumps({
        "lowerBound": data["lowerBound"],
        "upperBound": data["upperBound"],
        "result": number
    })
    client.broadcast_event("Number-Result", responsedata)
    return "200"

    
def random_number(lowerBound, upperBound):
    number = random.randint(lowerBound, upperBound)
    return number

def start_listener(port):
    host = cfg["client"]["ip"]
    app.run(host=host, port=port)