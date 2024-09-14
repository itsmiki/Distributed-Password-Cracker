import requests
import configparser
from config import GeneralConfig
from time import sleep
import json


class ClientInstance():
    def __init__(self, general_config: configparser.SectionProxy) -> None:
        self.general_config = general_config
    
    
    def connect_to_server(self) -> str:
        res = requests.get(f"http://{self.general_config['taskServerIp']}:{self.general_config['taskServerPort']}/api/v1/client/connect/{self.general_config['clientName']}")
        _general_config = GeneralConfig("config.ini")
        _general_config.set_client_id(str(res.text))
        return res.text


    def disconnect_from_server(self, client_id) -> None:
        res = requests.get(f"http://{self.general_config['taskServerIp']}:{self.general_config['taskServerPort']}/api/v1/client/disconnect/{client_id}")
        # _general_config = GeneralConfig("config.ini")
        # _general_config.delete_client_id()

    def get_task(self, client_id) -> tuple:
        res = requests.get(f"http://{self.general_config['taskServerIp']}:{self.general_config['taskServerPort']}/api/v1/client/get-task/{client_id}")
        _data = res.json()
        if _data['subtask_id'] == None:
            return _data, False
        
        if _data['attack_type'] == "mask":
            _file_masks_output = open(f"{self.general_config['tempDir']}{_data['subtask_id']}_mask.txt", 'a')
            _file_masks_input = open(f"{self.general_config['masksDir']}{_data['config']['mask']}", 'r')
            
            _all_masks = _file_masks_input.readlines()

            for line in range(_data["config"]['start'], _data["config"]['end']):
                _file_masks_output.write(_all_masks[line])
            
            _file_masks_output.close()
            _file_masks_input.close()
            _data['mask_file'] = f"{_data['subtask_id']}_mask.txt"
        
        _file = open(f"{self.general_config['tempDir']}{_data['task_id']}_output.txt", 'w')
        _file.close()

        _file = open(f"{self.general_config['tempDir']}{_data['task_id']}_hash.txt", 'w')
        _file.write(_data['hash'])
        _file.close()

        _data['hash_file'] = f"{_data['task_id']}_hash.txt"
        _data['output_file'] = f"{_data['task_id']}_output.txt"

        return _data, True

    def return_task(self, subtask_id):
        _file = open(f"{self.general_config['tempDir']}{subtask_id[:36]}_output.txt", 'r')
        _hash = _file.read()
        _file.close()
        
        _data = {
                "hashplaintext": _hash,
                "subtask": subtask_id
        }

        res = requests.post(f"http://{self.general_config['taskServerIp']}:{self.general_config['taskServerPort']}/api/v1/client/return-task", json=_data)

        return None




if __name__ == "__main__":
    client = ClientInstance(GeneralConfig("config.ini").get_config())
    # client.connect_to_server()
    print(client.get_task())
    #print(client.return_task('8fc97657-b9d0-4a52-8b9e-65ef838680971'))
    # client.disconnect_from_server() # ?? every second time doesnt work
