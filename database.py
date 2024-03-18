import mysql.connector
import helpers
import os

cfg = helpers.importyaml()

dburl = cfg["db"]["ip"]
dbuser = cfg["db"]["username"]
dbpass = cfg["db"]["password"]
dbname =  cfg["db"]["name"]

if os.getenv("RUNNING_IN_DOCKER"):
    dburl = "db"

def create_databases():
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS services(id INT AUTO_INCREMENT PRIMARY KEY, service_id VARCHAR(255), client_address VARCHAR(255), client_port INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS listeners(id INT AUTO_INCREMENT PRIMARY KEY, service_id VARCHAR(255), listener_id VARCHAR(255), event VARCHAR(255), listener_address VARCHAR(255))")

def register_service(serviceid, clientaddress, clientport):
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()

    sql = "INSERT INTO services (service_id, client_address, client_port) VALUES (%s, %s, %s)"
    val = (serviceid, clientaddress, int(clientport))
    cursor.execute(sql, val)

    db.commit()

def remove_service(serviceid):
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    sql = "DELETE FROM services WHERE service_id = %s"
    cursor.execute(sql, (serviceid,))

    db.commit()

def check_if_service_exists(service_id):
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    sql = "SELECT * FROM services WHERE service_id = %s"
    cursor.execute(sql, (service_id,))
    row = cursor.fetchone()
    print(row)
    return row != None

def get_client_address(service_id):
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    sql = "SELECT client_address FROM services WHERE service_id = %s"
    cursor.execute(sql, (service_id,))
    output = cursor.fetchone()
    result = "".join(output)
    return result

def get_client_port(service_id):
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    sql = "SELECT client_port FROM services WHERE service_id = %s"
    cursor.execute(sql, (service_id,))
    output = cursor.fetchone()
    result = "".join(str(output[0]))
    return result

def get_used_ports():
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    sql = "SELECT client_port FROM services"
    cursor.execute(sql)
    rows = cursor.fetchall()
    ports = []
    for row in rows:
        ports.append(int("".join(str(row[0]))))
    return ports
    

def register_listener(serviceid, listenerid, event, listeneraddress):
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    sql = "INSERT INTO listeners (service_id, listener_id, event, listener_address) VALUES (%s, %s, %s, %s)"
    val = (serviceid, listenerid, event, listeneraddress)
    cursor.execute(sql, val)

    db.commit()

def remove_listener(serviceid, listenerid):
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    sql = "DELETE FROM listeners WHERE service_id = %s AND listener_id = %s"
    val = (serviceid, listenerid)
    cursor.execute(sql, val)

    db.commit()

def get_listener_ids_by_service_id(serviceid):
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    sql = "SELECT listener_id FROM listeners WHERE service_id = %s"
    cursor.execute(sql, (serviceid,))
    rows = cursor.fetchall()
    newrows = []
    for row in rows:
        newrows.append("".join(row))
    return newrows

def get_listeners_by_event(event):
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    sql = "SELECT service_id, listener_id, event, listener_address FROM listeners WHERE event = %s"
    cursor.execute(sql, (event,))
    rows = cursor.fetchall()
    listeners = []
    for row in rows:
        listener = {"clientid": row[0], "listenerid": row[1], "event": row[2], "listener_address": row[3]}
        listeners.append(listener)
    return listeners

def get_all_services():
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    sql = "SELECT service_id, client_address, client_port FROM services"
    cursor.execute(sql)
    rows = cursor.fetchall()
    services = []
    for row in rows:
        service = {"service_id": row[0], "client_address": row[1], "client_port": row[2]}
        services.append(service)
    return services

if __name__ == "__main__":
    create_databases()