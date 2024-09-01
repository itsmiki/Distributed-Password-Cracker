from flask import (
    Blueprint, 
    request,
    jsonify
    )
from parser import TaskParser, HelperParser
from hashid import identify_hash

webadmin = Blueprint('webadmin', __name__, url_prefix='/api/v1/webadmin')

@webadmin.route('/create-task', methods=['POST'])
def create_task():
    # try:
    _data = request.get_json()
    identified_hash = identify_hash(_data['hash'])
    if identified_hash is False:
            return "Unprocessable Content", 422
    # print(_data)
    if _data['attack_type'] == "bruteforce":
        _bruteforce_task = TaskParser()
        _parent_id = _bruteforce_task.create_bruteforce_task(_data)
        _bruteforce_task.divide_bruteforce_task(_data, _parent_id, _data['hash_type'])
    elif _data['attack_type'] == "dictionary":
        _dictionary_task = TaskParser()
        _parent_id = _dictionary_task.create_dictionary_task(_data)
        _dictionary_task.divide_dictionary_task(_data, _parent_id, _data['hash_type'])
    elif _data['attack_type'] == "mask":
        _mask_task = TaskParser()
        _parent_id = _mask_task.create_mask_task(_data)
        _mask_task.divide_mask_task(_data, _parent_id, _data['hash_type'])
    
    return "Created", 201

    # except:
    #     return "Internal Server Error", 500
    
@webadmin.route('/remove-task/<task_id>', methods=['DELETE'])
def remove_task(task_id):
    try:
        _task_parser = TaskParser()
        _task_parser.remove_task(task_id)
        return "Ok", 200
    except:
        return "Internal Server Error", 500


@webadmin.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        _helper_parser = HelperParser()
        _tasks = _helper_parser.get_tasks()
        return jsonify(_tasks), 200
    except:
            return "Internal Server Error", 500

@webadmin.route('/hashes', methods=['GET'])
def get_hashes():
    try:
        _helper_parser = HelperParser()
        _hashes = _helper_parser.get_hashes()
        print(_hashes)
        return jsonify(_hashes), 200
    except:
        return "Internal Server Error", 500


@webadmin.route('/workers', methods=['GET'])
def get_workers():
    try:
        _helper_parser = HelperParser()
        _workers = _helper_parser.get_workers()
        return jsonify(_workers), 200
    except:
            return "Internal Server Error", 500
    
@webadmin.route('/masks', methods=['GET'])
def get_rules():
    try:
        _helper_parser = HelperParser()
        _masks = _helper_parser.get_masks()
        return jsonify(_masks), 200
    except:
            return "Internal Server Error", 500
    
@webadmin.route('/dictionaries', methods=['GET'])
def get_dictionaries():
    try:
        _helper_parser = HelperParser()
        _dictionaries = _helper_parser.get_dictionaries()
        print(_dictionaries)
        return jsonify(_dictionaries), 200
    except:
            return "Internal Server Error", 500

@webadmin.route('/identify-hash/<hash>', methods=['GET'])
def identify_hash(hash):
    try:
        identified_hash = identify_hash(hash, True)
        if identified_hash is False:
             return "Hash not supported or invalid", 404
        else:
             return identified_hash, 200
    except:
            return "Internal Server Error", 500