import requests
import helpers
import json
import atexit
import time
import listener

cfg = helpers.importyaml()

def register_service_with_server():
    address = "http://" + cfg["server"]["ip"] + ":" + str(cfg["server"]["port"])
    jsondata = json.dumps({
        "ClientID": "example-service", 
        "Action": "REGISTER", 
        "ClientAddress": cfg["client"]["ip"]
        })
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(address, data=jsondata, headers=headers)
    data = r.json()
    helpers.writeyaml("client", "port", data["Port"])
    print("Registered service")
    return data["Port"]

def register_listener_with_server():
    address = "http://" + cfg["server"]["ip"] + ":" + str(cfg["server"]["port"])
    headers = {
        "Content-Type": "application/json"
    }
    jsondata = json.dumps({
        "ClientID": "example-service",
        "Action": "REGLIST",
        "Event": "Generate-Number",
        "ListenerID": "on-generate-request",
        "ListenerEndpoint": "/listener"
    })
    r = requests.post(address, data=jsondata, headers=headers)
    print("Registered listener")

def remove_service_from_server():
    address = "http://" + cfg["server"]["ip"] + ":" + str(cfg["server"]["port"])
    headers = {
        "Content-Type": "application/json"
    }
    jsondata = json.dumps({
        "ClientID": "example-service",
        "Action": "REMOVE"
    })
    r = requests.post(address, data=jsondata, headers=headers)
    print("Removed service and listeners")

def broadcast_event(event, data):
    address = "http://" + cfg["server"]["ip"] + ":" + str(cfg["server"]["port"])
    headers = {
        "Content-Type": "application/json"
    }
    jsondata = json.dumps({
        "ClientID": "example-service",
        "Action": "BROADCAST",
        "Event": event,
        "Data": data
    })
    r = requests.post(address, data=jsondata, headers=headers)

def exit_handler():
    remove_service_from_server()

def setup():
    port = register_service_with_server()
    register_listener_with_server()
    atexit.register(exit_handler)
    listener.start_listener(port)

if __name__ == "__main__":
    setup()