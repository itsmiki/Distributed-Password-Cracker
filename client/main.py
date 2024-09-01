from config import HashcatConfig, GeneralConfig
import os
from clients import ClientInstance
from hashcat import HashcatInterface
from time import sleep
from sys import platform



def run_client():
    _workstation_name = input("Set name for this workstation:")

    if platform == "linux" or platform == "linux2":
        print("Detected system: Linux")
        hashcat_config = HashcatConfig("config.ini")
        hashcat_config.set_binary_dir(f'{os.path.dirname(os.path.realpath(__file__))}/hashcat')
        hashcat_config.set_binary_name("hashcat.bin")
        hashcat_config.set_wordlists_dir("../wordlists/")
        hashcat_config.set_temp_dir("../temp/")
        
        general_config = GeneralConfig("config.ini")
        general_config.set_run_command_prefix("./")
        general_config.set_task_server_ip("192.168.100.98")
        general_config.set_task_server_port("7000")
        general_config.set_client_name(_workstation_name)
        general_config.set_temp_dir("temp/")
        general_config.set_masks_dir("hashcat/rules/")
    elif platform == "darwin":
        print("Detected system: macOS")
        pass
    elif platform == "win32":
        print("Detected system: Windows")
        hashcat_config = HashcatConfig("config.ini")
        hashcat_config.set_binary_dir(f'{os.path.dirname(os.path.realpath(__file__))}\\hashcat')
        hashcat_config.set_binary_name("hashcat.exe")
        hashcat_config.set_wordlists_dir("..\\wordlists\\")
        hashcat_config.set_temp_dir("..\\temp\\")
        
        general_config = GeneralConfig("config.ini")
        general_config.set_run_command_prefix(".\\")
        general_config.set_task_server_ip("192.168.100.98")
        general_config.set_task_server_port("7000")
        general_config.set_client_name(_workstation_name)
        general_config.set_temp_dir("temp\\")
        general_config.set_masks_dir("hashcat\\rules\\")

    _client_instance = ClientInstance(GeneralConfig("config.ini").get_config())
    _client_id = _client_instance.connect_to_server()
    _hashcat_interface = HashcatInterface(HashcatConfig("config.ini").get_config(), GeneralConfig("config.ini").get_config())

    print(_client_id)
    while(1):
        _task_data, _is_data = _client_instance.get_task(_client_id)

        if _is_data is False:
            print("Idle...")
            sleep(5)
            continue
        
        print("Got task!")
        print(_task_data)

        if _task_data['attack_type'] == 'bruteforce':
            _hashcat_interface.bruteforce_attack(
                _task_data["config"]["hash_type"], 
                _task_data["hash_file"], 
                _task_data["output_file"],
                _task_data["config"]["charset"],
                _task_data["config"]["pattern"]
                )
        
        if _task_data['attack_type'] == 'dictionary':
            _hashcat_interface.dictionary_attack(
                _task_data["config"]["hash_type"], 
                _task_data["hash_file"], 
                _task_data["output_file"],
                _task_data["config"]["dictionary"]
                )
            
        if _task_data['attack_type'] == 'mask':
            _hashcat_interface.mask_attack(
                _task_data["config"]["hash_type"], 
                _task_data["hash_file"], 
                _task_data["output_file"],
                _task_data["config"]["dictionary"],
                _task_data["mask_file"]
                )
        
        _client_instance.return_task(_task_data['subtask_id'])


if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("Disconnected from server!")
        _config = GeneralConfig("config.ini").get_config()
        _client_instance = ClientInstance(_config)
        _client_instance.disconnect_from_server(_config['clientId'])


