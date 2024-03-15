import helpers
import database
from flask import Flask, request

cfg = helpers.importyaml()
database.create_databases()

serverhost = cfg["server"]["ip"]
serverport = cfg["server"]["port"]

app = Flask(__name__)

@app.route("/", methods=["POST"])
def incomingrequest():
    json = request.get_json()
    clientid = json["ClientID"]
    action = json["Action"]

    match action:
        case "REGISTER":
            address = json["ClientAddress"]
            print(f"REGISTER: {clientid}, {address}")
            database.register_service(clientid, address)
        case "REMOVE":
            print(f"REMOVE: {clientid}")
            database.remove_service(clientid)

    return(json)


app.run(host=serverhost, port=serverport)