# Importing all needed modules.
from flask import Flask, request
from models.electro_scooter import ElectroScooter
from raft import RAFTFactory
from models.database import db
import time
import random
from flask_swagger_ui import get_swaggerui_blueprint

# Defining the service credentials.
service_info = {
    "host" : "127.0.0.1",
    "port" : 8000
}

# Stopping the start up of the service for a couple of seconds to chose a candidate.
time.sleep(random.randint(1, 3))

# Creating the CRUD functionalities.
crud = RAFTFactory(service_info).create_server()

# Creating the flask application.
app = Flask(__name__)

# Configure sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_service_1.db'

# Connect to db
db.init_app(app)

with app.app_context():
    # Create the database tables
    db.create_all()

print("connected")


# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Electro Scooter API"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

@app.route('/api/electro-scooters', methods=['POST'])
def create_electro_scooter():
    headers = dict(request.headers)
    if not crud.leader and ("Token" not in headers or headers["Token"] != "Leader"):
        return {
            "error" : "Access denied!"
        }, 403
    else:
        data = request.get_json()
        return_dict, status_code = crud.create(data)
        return return_dict, status_code


@app.route('/api/electro-scooters', methods=['GET'])
def get_electro_scooters():
    return_dict, status_code = crud.get_all()
    return return_dict, status_code


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['GET'])
def get_electro_scooter_by_id(scooter_id):
    return_dict, status_code = crud.get_by_id(scooter_id)
    return return_dict, status_code


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['PUT'])
def update_electro_scooter(scooter_id):
    headers = dict(request.headers)
    if not crud.leader and ("Token" not in headers or headers["Token"] != "Leader"):
        return {
            "error" : "Access denied!"
        }, 403
    else:
        data = request.get_json()
        return_dict, status_code = crud.update(scooter_id, data)
        return return_dict, status_code   


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['DELETE'])
def delete_electro_scooter(scooter_id):
    headers = dict(request.headers)
    if not crud.leader and ("Token" not in headers or headers["Token"] != "Leader"):
        return {
            "error" : "Access denied!"
        }, 403
    else:
        password = request.headers.get('X-Delete-Password')
        if password == 'qwerty':
            return_dict, status_code = crud.delete(scooter_id)
            return return_dict, status_code 

app.run(
    host = service_info["host"],
    port = service_info["port"]
)