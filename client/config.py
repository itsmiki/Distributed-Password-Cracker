import configparser
import os
from utlis import ConfigClass


class HashcatConfig(ConfigClass):
    def __init__(self, config_path: str) -> None:
        super().__init__(config_path)
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        self.create_section()
        self.save_config()

    def set_binary_name(self, binary_path: str) -> None:
        self.config.read(self.config_path)
        self.config.set('HASHCAT', 'binaryName', binary_path)
        self.save_config()

    def set_binary_dir(self, binary_dir: str) -> None:
        self.config.read(self.config_path)
        self.config.set('HASHCAT', 'binaryDir', binary_dir)
        self.save_config()

    def set_wordlists_dir(self, wordlist_dir: str) -> None:
        self.config.read(self.config_path)
        self.config.set('HASHCAT', 'wordlistDir', wordlist_dir)
        self.save_config()

    def set_temp_dir(self, temp_dir) -> None:
        self.config.read(self.config_path)
        self.config.set('HASHCAT', 'tempDir', temp_dir)
        self.save_config()
    
    def save_config(self) -> None:
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

    def get_config(self) -> configparser.SectionProxy:
        return self.config['HASHCAT']
    
    def create_section(self):
        try:
            self.config.add_section('HASHCAT')
        except:
            print(u'Config already exists, loaded.')

class GeneralConfig(ConfigClass):
    def __init__(self, config_path: str) -> None:
        super().__init__(config_path)
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        self.create_section()
        self.save_config()

    def set_run_command_prefix(self, run_command_prefix: str) -> None:
        self.config.read(self.config_path)
        self.config.set('GENERAL', 'runCommandPrefix', run_command_prefix)
        self.save_config()

    def set_task_server_ip(self, ip: str) -> None:
        self.config.read(self.config_path)
        self.config.set('GENERAL', 'taskServerIp', ip)
        self.save_config()

    def set_task_server_port(self, port: str) -> None:
        self.config.read(self.config_path)
        self.config.set('GENERAL', 'taskServerPort', port)
        self.save_config()

    def set_client_name(self, name: str) -> None:
        self.config.read(self.config_path)
        self.config.set('GENERAL', 'clientName', name)
        self.save_config()

    def set_client_id(self, client_id: str) -> None:
        self.config.read(self.config_path)
        self.config.set('GENERAL', 'clientId', client_id)
        self.save_config()
    
    def delete_client_id(self) -> None:
        self.config.read(self.config_path)
        self.config.remove_option('GENERAL', 'clientId')
        self.save_config()

    def set_temp_dir(self, temp_dir) -> None:
        self.config.read(self.config_path)
        self.config.set('GENERAL', 'tempDir', temp_dir)
        self.save_config()

    def set_masks_dir(self, masks_dir) -> None:
        self.config.read(self.config_path)
        self.config.set('GENERAL', 'masksDir', masks_dir)
        self.save_config()
    
    def save_config(self) -> None:
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

    def get_config(self) -> configparser.SectionProxy:
        return self.config['GENERAL']
    
    def create_section(self):
        try:
            self.config.add_section('GENERAL')
        except:
            print(u'Config already exists, loaded.')


if __name__=="__main__":
    hashcat_config = HashcatConfig("config.ini")
    hashcat_config.set_binary_dir(f'{os.path.dirname(os.path.realpath(__file__))}\\hashcat')
    hashcat_config.set_binary_name("hashcat.exe")
    hashcat_config.set_wordlists_dir("..\\wordlists\\")
    hashcat_config.set_temp_dir("..\\temp\\")
    # print(hashcat_config.get_config())
    
    general_config = GeneralConfig("config.ini")
    general_config.set_run_command_prefix(".\\")
    general_config.set_task_server_ip("192.168.100.98")
    general_config.set_task_server_port("7000")
    general_config.set_client_name("Computer 1")
    general_config.set_temp_dir("temp\\")