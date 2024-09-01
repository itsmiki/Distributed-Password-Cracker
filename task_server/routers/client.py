from flask import (
    Blueprint, 
    request, 
    )
from parser import ClientParser

client = Blueprint('client', __name__, url_prefix='/api/v1/client')

@client.route('/connect/<name>', methods=['GET'])
def connect(name):
    _clientparser = ClientParser()
    _client_id = _clientparser.connect_client(request.remote_addr, name)

    return _client_id, 200

@client.route('/disconnect/<client_id>', methods=['GET'])
def disconnect(client_id):
    _clientparser = ClientParser()
    _client_id = _clientparser.disconnect_client(client_id)

    return _client_id, 200


@client.route('/get-task/<client_id>', methods=['GET'])
def get_task(client_id):
    _clientparser = ClientParser()
    _client_data = _clientparser.assign_task(client_id)
    return _client_data, 200


@client.route('/return-task', methods=['POST'])
def return_task():
    _data = request.get_json()
    print(_data)
    _clientparser = ClientParser()
    _clientparser.parse_returned_task(_data['subtask'], _data['hashplaintext'])
    print(_data)

    return "Ok", 200

