from enum import Enum

class AttackType(Enum):
    dictionary = 1
    bruteforce = 2
    mask = 3

class HashType(Enum):
    MD5 = 0
    SHA1 = 100
    SHA2_256 = 1400
    SHA2_512 = 1700
    SHA3_256 = 17400
    SHA3_512 = 17600

class AttackConfig():
    pass

from abc import ABC, abstractmethod
from accessify import private

class ConfigClass(ABC):
    def __init__(self, config_path: str):
        self.config_path = config_path
    
    @abstractmethod
    def get_config(self):
        pass

    @private
    @abstractmethod
    def save_config(self):
        pass
    
    @private
    @abstractmethod
    def create_section(self):
        pass
