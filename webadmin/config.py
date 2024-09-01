import configparser
from utils import ConfigClass

class GeneralConfig(ConfigClass):
    def __init__(self, config_path: str) -> None:
        super().__init__(config_path)
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        self.create_section()
        self.save_config()

    def set_task_server_ip(self, ip: str) -> None:
        self.config.read(self.config_path)
        self.config.set('GENERAL', 'taskServerIp', ip)
        self.save_config()

    def set_task_server_port(self, port: str) -> None:
        self.config.read(self.config_path)
        self.config.set('GENERAL', 'taskServerPort', port)
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
    general_config = GeneralConfig("config.ini")
    general_config.set_task_server_ip("192.168.100.98")
    general_config.set_task_server_port("7000")

