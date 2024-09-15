from models import Tasks, SubTasks, Clients, Hashes
from server import db
import uuid
import json
from utils import HashType
import time
from uuid_extensions import uuid7
import math



class TaskParser():
    def __init__(self):
        self.length = {
            "?l": 26,
            "?l?d": 36,
            "?l?u": 52,
            "?l?u?d": 62,
            "?l?u?d?s": 95
        }
        self.charsets = {
            "?l": "abcdefghijklmnopqrstuvwxyz",
            "?l?d": "abcdefghijklmnopqrstuvwxyz0123456789",
            "?l?u": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "?l?u?d": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            "?l?u?d?s": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        }

    def create_bruteforce_task(self, task_data: dict) -> str:
        _task_id = str(uuid7())
        _new_task = Tasks(
            task_id = _task_id,
            attack_type = task_data['attack_type'],
            hash_type = task_data['hash_type'],
            hash = task_data['hash'],
            number_of_subtasks = None,
            subtasks_done = 0,
            config = json.dumps({"charset": task_data['charset'], "length": task_data['length']}),
            time_started = time.time(),
            time_finished = None,
            hash_found = 0,
            is_deleted = 0
            )
        db.session.add(_new_task)
        db.session.commit()

        return _task_id
    
    def divide_bruteforce_task(self, task_data: dict, parent_id: str, hash_type: str):
        with open("config_bruteforce_attack.json") as file: 
            parsing_rules = json.load(file)

        charset_2 = {}
        i = 0

        for character in self.charsets[task_data['charset']]:
            try:
                charset_2[i % parsing_rules[HashType(int(task_data['hash_type'])).name][task_data['charset']][task_data['length']]] += character
            except:
                charset_2[i % parsing_rules[HashType(int(task_data['hash_type'])).name][task_data['charset']][task_data['length']]] = character
            i += 1

        # print(charset_2)
        if parsing_rules[HashType(int(task_data['hash_type'])).name][task_data['charset']][task_data['length']] == 1:
            _pattern = f"{'?1' * int(task_data['length'])} --increment"
            _number_of_tasks = 1
            _new_task = SubTasks(
                subtask_id = parent_id + "0",
                parent_id = parent_id,
                config = json.dumps({"charset": [task_data['charset'], task_data['charset']], "pattern": _pattern, "hash_type": hash_type}),
                client_id = None
                )
            db.session.add(_new_task)
        else:
            _pattern_increment = f"{'?1' * (int(task_data['length']) - 1)} --increment"
            _number_of_tasks = parsing_rules[HashType(int(task_data['hash_type'])).name][task_data['charset']][task_data['length']] + 1
            _new_task = SubTasks(
                subtask_id = parent_id + "0",
                parent_id = parent_id,
                config = json.dumps({"charset": [task_data['charset'], charset_2[0]], "pattern": _pattern_increment, "hash_type": hash_type}),
                client_id = None
                )
            db.session.add(_new_task)
            
            for _number in range(0, _number_of_tasks - 1):
                _pattern = f"{'?1' * (int(task_data['length']) - 1)}?2"
                _new_task = SubTasks(
                    subtask_id = parent_id + str(_number + 1),
                    parent_id = parent_id,
                    config = json.dumps({"charset": [task_data['charset'], charset_2[_number]], "pattern": _pattern, "hash_type": hash_type}),
                    client_id = None
                    )
                db.session.add(_new_task)
        
        _parent_task = Tasks.query.filter_by(task_id=parent_id).first()
        _parent_task.number_of_subtasks = _number_of_tasks

        db.session.commit()
    
    def create_dictionary_task(self, task_data: dict) -> str:
        _task_id = str(uuid7())
        _new_task = Tasks(
            task_id = _task_id,
            attack_type = task_data['attack_type'],
            hash_type = task_data['hash_type'],
            hash = task_data['hash'],
            number_of_subtasks = None,
            subtasks_done = 0,
            config = json.dumps({"dictionaries": task_data['dictionaries']}),
            time_started = time.time(),
            time_finished = None,
            hash_found = 0,
            is_deleted = 0
            )
        db.session.add(_new_task)
        db.session.commit()

        return _task_id
    
    def divide_mask_task(self, task_data: dict, parent_id: str, hash_type: str):
        with open("config_mask_attack.json") as file: 
            _parsing_rules = json.load(file)

        with open("config_masks.json") as file: 
            _masks_config = json.load(file)

        _number_of_masks = 0
        _mask_number = 0
        for _mask in task_data['masks']:
            _number_of_masks += _masks_config[task_data['masks'][_mask_number]]
            _mask_number += 1

        if (_number_of_masks / _parsing_rules[HashType(int(task_data['hash_type'])).name]["max_mask_number"]) > _parsing_rules[HashType(int(task_data['hash_type'])).name]["min_task_number"]:
            _number_of_division_parts = math.ceil(_number_of_masks / _parsing_rules[HashType(int(task_data['hash_type'])).name]["max_mask_number"])
        else:
            _number_of_division_parts = _parsing_rules[HashType(int(task_data['hash_type'])).name]["min_task_number"]


        _division_points_of_masks = [0]
        for _division in range (1, _number_of_division_parts):
            _division_points_of_masks.append(int(_number_of_masks / _number_of_division_parts * _division))
        _division_points_of_masks.append(_number_of_masks)


        _number_of_tasks = _number_of_division_parts

        for _task_number in range(0, _number_of_tasks):
            _new_task = SubTasks(
                subtask_id = parent_id + str(_task_number),
                parent_id = parent_id,
                config = json.dumps({"dictionary": task_data['dictionaries'][0], 
                                     "mask": task_data['masks'][0],
                                     "start": _division_points_of_masks[_task_number],
                                     "end":  _division_points_of_masks[_task_number + 1],
                                     "hash_type": hash_type}),
                client_id = None
                )
            db.session.add(_new_task)
        
        
        _parent_task = Tasks.query.filter_by(task_id=parent_id).first()
        _parent_task.number_of_subtasks = _number_of_tasks

        db.session.commit()
    
    def create_mask_task(self, task_data: dict) -> str:
        _task_id = str(uuid7())
        _new_task = Tasks(
            task_id = _task_id,
            attack_type = task_data['attack_type'],
            hash_type = task_data['hash_type'],
            hash = task_data['hash'],
            number_of_subtasks = None,
            subtasks_done = 0,
            config = json.dumps({"dictionaries": task_data['dictionaries'], "masks": task_data['masks']}),
            time_started = time.time(),
            time_finished = None,
            hash_found = 0,
            is_deleted = 0
            )
        db.session.add(_new_task)
        db.session.commit()

        return _task_id
    
    def divide_dictionary_task(self, task_data: dict, parent_id: str, hash_type: str):
        _number_of_tasks = len(task_data['dictionaries'])

        for _task_number in range(0, _number_of_tasks):
            _new_task = SubTasks(
                subtask_id = parent_id + str(_task_number),
                parent_id = parent_id,
                config = json.dumps({"dictionaries": task_data['dictionaries'][_task_number], "hash_type": hash_type}),
                client_id = None
                )
            db.session.add(_new_task)
        
        
        _parent_task = Tasks.query.filter_by(task_id=parent_id).first()
        _parent_task.number_of_subtasks = _number_of_tasks

    def remove_task(self, task_id: dict) -> str:
        _subtasks = SubTasks.query.filter_by(parent_id = task_id).delete()
        # _hashes = Hashes.query.filter_by(task_id = task_id).update({Hashes.task_id: None})
        _tasks = Tasks.query.filter_by(task_id = task_id).update({Tasks.is_deleted: 1})
        db.session.commit()

        return task_id
    
    


class ClientParser():
    def __init__(self):
        pass
    
    def connect_client(self, client_ip: str, name: str) -> str:
        _client_id = str(uuid7())
        _new_client = Clients(
            client_id = _client_id,
            name = name,
            client_ip = client_ip
            )
        db.session.add(_new_client)
        db.session.commit()

        return _client_id


    def disconnect_client(self, client_id: str) -> str:
        _subtasks = SubTasks.query.filter_by(client_id=client_id).update({SubTasks.client_id: None})

        _client = Clients.query.filter_by(client_id=client_id).first()
        db.session.delete(_client)
        db.session.commit()

        return client_id

    def assign_task(self, client_id: str):
        _task = SubTasks.query.filter_by(client_id=None).first()
        if _task is None:
            _data = {
            "subtask_id": None
            }
            return _data
        
        _parent_task = Tasks.query.filter_by(task_id=_task.parent_id).first()
        _data = {
            "subtask_id": _task.subtask_id,
            "task_id": _task.parent_id,
            "attack_type": _parent_task.attack_type,
            "hash": _parent_task.hash,
            "config": json.loads(_task.config)
            }
        
        _task.client_id = client_id
        db.session.commit()
        
        return _data
    
    def parse_returned_task(self, subtask_id, hash_plaintext):
        try:
            _task = SubTasks.query.filter_by(subtask_id=subtask_id).first()
            db.session.delete(_task)

            _parent_task = Tasks.query.filter_by(task_id=_task.parent_id).first()

            if _parent_task.subtasks_done + 1 == _parent_task.number_of_subtasks:
                 _parent_task.time_finished = time.time()

            _parent_task.subtasks_done += 1

            if hash_plaintext != "":
                _hash_data = hash_plaintext.split(':')
                _found_hash = Hashes(
                    hash_id = str(uuid7()),
                    task_id = _parent_task.task_id,
                    hash = _hash_data[0],
                    plaintext = _hash_data[1].rstrip('\n')
                )
                db.session.add(_found_hash)

                _parent_task.time_finished = time.time()
                _parent_task.hash_found = 1

                _task = SubTasks.query.filter_by(parent_id=_parent_task.task_id).delete()

            db.session.commit()

        except:
            print("Already found!")
            return None
    

        
class HelperParser():
    def __init__(self) -> None:
        pass
        
    def get_workers(self):
        _workers = Clients.query.all()
        _workers_list = []
        for _worker in _workers:
            _dict = _worker.__dict__
            del _dict['_sa_instance_state']
            _workers_list.append(_dict)
    
        return _workers_list
    
    def get_tasks(self):
        _tasks = Tasks.query.all()
        _tasks_list = []
        for _task in _tasks:

            _dict = _task.__dict__
            del _dict['_sa_instance_state']

            _hash_data = Hashes.query.filter_by(task_id = _task.task_id).first()
            if _hash_data is not None:
                _dict['password'] = _hash_data.plaintext
            else:
                _dict['password'] = "NOT FOUND"

            if _dict["is_deleted"] == 0:
                _tasks_list.append(_dict)
    
        return _tasks_list
    
    def get_hashes(self):
        _hashes = Hashes.query.all()
        _hashes_list = []
        for _hash in _hashes:
            _dict = _hash.__dict__
            # print(_dict)
            del _dict['_sa_instance_state']
            # print(_dict)
            _task_data = Tasks.query.filter_by(task_id = _hash.task_id).first()
            _dict['hash_type'] = HashType(_task_data.hash_type).name
            _hashes_list.append(_dict)
            # print(_dict)
        
        return _hashes_list

    def get_masks(self):
        with open("config_masks.json") as file: 
            rules = json.load(file)
            return rules
        
    def get_dictionaries(self):
        with open("config_dictionaries.json") as file: 
            rules = json.load(file)
            return rules





if __name__ =="__main__":
    pass
    taskparser = TaskParser()
    taskparser.divide_bruteforce_task_v2({'attack_type': 'bruteforce', 
                                          'hash': 'bruteforce', 
                                          'hash_type': '0', 
                                          'length': '7', 
                                          'charset': '?l?u'}, 
                                          "858d65f0-6186-417b-9026-04246b6d6787", 
                                          0)
