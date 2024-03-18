import helpers
import requests
import database
import json
import os

cfg = helpers.importyaml()

def register_service(clientid, address):
    used_ports = database.get_used_ports()
    used_ports.append(cfg["server"]["port"])
    used_ports = sorted(used_ports)
    last_port = used_ports[-1]
    port = last_port + 1
    database.register_service(clientid, address, port)
    return port

def send_data(clientid, victimid, data):
    victim_address = database.get_client_address(victimid)
    jsondata = {
        "source": clientid,
        "action": "SEND",
        "data": data
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(victim_address, data=jsondata, headers=headers)
    return r.status_code

def send_kill(clientid, victimid, data):
    victim_address = database.get_client_address(victimid)
    jsondata = {
        "source": clientid,
        "action": "KILL",
        "data": data
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(victim_address, data=jsondata, headers=headers)
    return r.status_code

def register_listener(clientid, listenerid, event, listeneraddress):
    database_exists = database.check_if_service_exists(clientid)
    if database_exists:
        database.register_listener(clientid, listenerid, event, listeneraddress)
        return 200
    else:
        return 404

def remove_service(clientid):
    listeners = database.get_listener_ids_by_service_id(clientid)
    for listenerid in listeners:
        database.remove_listener(clientid, listenerid)
    database.remove_service(clientid)

def broadcast_event(clientid, event, data):
    database_exists = database.check_if_service_exists(clientid)
    if database_exists:
        listeners = database.get_listeners_by_event(event)
        for listener in listeners:
            clientaddress = database.get_client_address(clientid)
            clientport = database.get_client_port(listener["clientid"])
            if os.getenv("RUNNING_IN_DOCKER"):
                clientaddress = "host.docker.internal"
            endpointurl = "http://" + clientaddress + ":" + clientport + listener["listener_address"]
            jsondata = json.dumps({
                "source": clientid,
                "event": event,
                "data": data
            })
            headers = {
                "Content-Type": "application/json"
            }
            r = requests.post(endpointurl, data=jsondata, headers=headers)
            print(f"Event sent - from: {clientid} - to: {endpointurl} - event: {event} - status: {r.status_code}")

def interval_wellness_check():
    services = database.get_all_services()
    for service in services:
        clientid = service["clientid"]
        clientaddress = database.get_client_address(clientid)
        clientport = database.get_client_port(clientid)
        if os.getenv("RUNNING_IN_DOCKER"):
            clientaddress = "host.docker.internal"
        endpointurl = "http://" + clientaddress + ":" + clientport + "/up"
        r = requests.get(endpointurl)
        print(f"Wellness check - client: {clientid} - status: {r.status_code}")
        if r.status_code != 200:
            remove_service(clientid)
            print(f"Client {clientid} removed due to wellness check failure")