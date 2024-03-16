import helpers
import database
import actions
import os
from flask import Flask, request

cfg = helpers.importyaml()
database.create_databases()
print("Database connection valid")

if os.getenv("RUNNING_IN_DOCKER"):
    print("Docker detected")

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
            port = actions.register_service(clientid, address)
            print(f"REGISTER: {clientid}, {address}, {port}")
            json["Port"] = port
        case "REMOVE":
            print(f"REMOVE: {clientid}")
            actions.remove_service(clientid)
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
        case "REGLIST":
            listenerid = json["ListenerID"]
            listenerendpoint = json["ListenerEndpoint"]
            event = json["Event"]
            status = actions.register_listener(clientid, listenerid, event, listenerendpoint)
            print(f"REGLIST: {clientid}, {listenerid}, {event}, {listenerendpoint}, {status}")
            json["status"] = status
        case "REMOVELIST":
            listenerid = json["ListenerID"]
            database.remove_listener(clientid, listenerid)
            print(f"REMOVELIST: {clientid}, {listenerid}")
        case "BROADCAST":
            event = json["Event"]
            data = json["Data"]
            actions.broadcast_event(clientid, event, data)
            print(f"BROADCAST: {clientid}, {event}")
            
    return(json)

@app.route("/up", methods=["GET"])
def wellness_check():
    return {"status": "200"}

if __name__ == "__main__":
    debug = cfg["server"]["debug"]
    app.run(debug=debug, host=serverhost, port=serverport)