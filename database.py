import mysql.connector
import helpers

cfg = helpers.importyaml()

dburl = cfg["db"]["ip"]
dbuser = cfg["db"]["username"]
dbpass = cfg["db"]["password"]
dbname =  cfg["db"]["name"]

def create_databases():
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS services(ID INT AUTO_INCREMENT PRIMARY KEY, service_id VARCHAR(255), client_address VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS listeners(ID INT AUTO_INCREMENT PRIMARY KEY, service_id VARCHAR(255), listener_id VARCHAR(255), event VARCHAR(255), listener_address VARCHAR(255))")

def register_service(serviceid, clientaddress):
    db = mysql.connector.connect(
        host = dburl,
        user = dbuser,
        password = dbpass,
        database = dbname
    )

    cursor = db.cursor()

    sql = "INSERT INTO services (service_id, client_address) VALUES (%s, %s)"
    val = (serviceid, clientaddress)
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

create_databases()