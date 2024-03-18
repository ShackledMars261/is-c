# IS-C - InterScript-Communications
A modular service for communication between scripts and services

# Features:
- No more worrying about dynamic ips, all network information is gathered for you
- Event and Event Listeners for communication between connected services
- Runs both in and out of Docker

# Setup
1. Download and setup Docker Desktop
2. ```git clone git@github.com:ShackledMars261/is-c.git```
3. ```docker-compose up -d --build```
### Running Server in Docker:
4. Make sure both services start up
5. Connect your service
### Running Server outside Docker:
4. Stop the app service (leave the db service running, unless you're using a local install of MySQL)
5. ```cd is-c```
6. ```pip install -r requirements.txt```
7. ```python server.py```
8. Connect your service

# Creating a service
- A sample service is provided in the examples directory

# Requests
- A postman collection with the major requests is provided in the examples directory

# TODO
- Fix bugs
- Come up with name (current one is pretty trash)
- Update README
- Use more features in the example
- Update wellness check to check connected services (new client endpoint)
- GETIP and GETPORT actions (for clients)
- 
