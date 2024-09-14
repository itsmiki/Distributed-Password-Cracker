from config import HashcatConfig, GeneralConfig
import os
from clients import ClientInstance
from hashcat import HashcatInterface
from time import sleep
from sys import platform
from utlis import print_dict, move_terminal
import colorama
from colorama import Fore, Back, Style


def run_client():
    colorama.init(autoreset=True)

    _workstation_name = input("Set name for this workstation: ")
    _server_ip = input("Provide server IP: ")
    _server_port = input("Provide server port: ")

    if platform == "linux" or platform == "linux2":
        print("Detected system: Linux")
        hashcat_config = HashcatConfig("config.ini")
        hashcat_config.set_binary_dir(f'{os.path.dirname(os.path.realpath(__file__))}/hashcat')
        hashcat_config.set_binary_name("hashcat.bin")
        hashcat_config.set_wordlists_dir("../wordlists/")
        hashcat_config.set_temp_dir("../temp/")
        
        general_config = GeneralConfig("config.ini")
        general_config.set_run_command_prefix("./")
        general_config.set_task_server_ip(_server_ip)
        general_config.set_task_server_port(_server_port)
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
        general_config.set_task_server_ip(_server_ip)
        general_config.set_task_server_port(_server_port)
        general_config.set_client_name(_workstation_name)
        general_config.set_temp_dir("temp\\")
        general_config.set_masks_dir("hashcat\\rules\\")

    _client_instance = ClientInstance(GeneralConfig("config.ini").get_config())
    
    try:
        _client_id = _client_instance.connect_to_server()
        print(Fore.GREEN + Style.BRIGHT + "Connected to server!")
    except:
        print(Fore.RED + Style.BRIGHT + "Server unavailable, please check if the IP address provided was correct.")


    _hashcat_interface = HashcatInterface(HashcatConfig("config.ini").get_config(), GeneralConfig("config.ini").get_config())

    print(Fore.BLUE + Style.BRIGHT + "Client ID: " + _client_id)
    sleep(2)
    while(1):
        _task_data, _is_data = _client_instance.get_task(_client_id)

        if _is_data is False:
            print("Idle...")
            sleep(5)
            continue
        
        move_terminal(os.get_terminal_size().lines)
        print(Fore.BLUE + Style.BRIGHT + f"You are cracking on {_workstation_name} with id {_client_id}.")
        print(Fore.GREEN + Style.BRIGHT + "Task recieved!")
        print("\033[1m" + "++++===============================TASK DATA===============================++++  " + "\033[0m")
        print_dict(_task_data)
        print("\033[1m" + "++++=======================================================================++++\n" + "\033[0m")
        print(Fore.GREEN + Style.BRIGHT + "Cracking started.")

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
        print(Fore.RED + Style.BRIGHT + "Disconnected from server!")
        _config = GeneralConfig("config.ini").get_config()
        _client_instance = ClientInstance(_config)
        _client_instance.disconnect_from_server(_config['clientId'])


