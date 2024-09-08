import os
import sys
import configparser

arguments = {
    "mask_update": "Synchronizes data in 'task_server/config_masks.json'.",
    "dictionary_update": "Synchronizes data in 'task_server/config_dictionaries.json'.",
    "server_ip <ip> <port>": "Synchronizes data in 'client/config.ini' and 'webadmin/config.ini'."
}

def print_help():
    for key in arguments:
        print(f"{key} - {arguments[key]}")

def sync_masks():
    path = f"{os.path.dirname(os.path.realpath(__file__))}\\hashcat\\rules"
    dir_list = os.listdir(path)
    print(f"Files and directories in '{path}' :")
    print(dir_list)
    config = {}

    dir_list.remove("hybrid")

    for dir in dir_list:
        with open(f"{path}\\{dir}", "r", encoding="utf8") as f:
            config[dir] = len(f.readlines())


def sync_wordlists():
    path = f"{os.path.dirname(os.path.realpath(__file__))}\\client\\wordlists"
    dir_list = os.listdir(path)
    print(f"Files and directories in '{path}' :")
    print(dir_list)
    config = {}

    for dir in dir_list:
        with open(f"{path}\\{dir}", "r", encoding="utf8") as f:
            config[dir] = len(f.readlines())

def change_server_data(ip, port):
    client_config = 'client\\config.ini'
    config = configparser.ConfigParser()
    config.read(client_config)
    config.set('GENERAL', 'taskServerIp', ip)
    config.set('GENERAL', 'taskServerPort', port)
    with open(client_config, 'w') as configfile:
            config.write(configfile)

    webadmin_config = 'webadmin\\config.ini'
    config = configparser.ConfigParser()
    config.read(webadmin_config)
    config.set('GENERAL', 'taskServerIp', ip)
    config.set('GENERAL', 'taskServerPort', port)
    with open(webadmin_config, 'w') as configfile:
            config.write(configfile)

    

if __name__ =="__main__":
    if sys.argv[1] == "mask_update":
        sync_masks()
    elif sys.argv[1] == "dictionary_update":
        sync_wordlists()
    elif sys.argv[1] == "server_ip":
        change_server_data(sys.argv[2], sys.argv[3])
    else:
        print("Wrong argument!\n")
        print_help()
        print("\n")
