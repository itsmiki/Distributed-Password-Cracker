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

def parse_charset(keys: list):
    _charset = ""
    if 'lowercase' in keys:
        _charset += "?l"
    if 'uppercase' in keys:
        _charset += "?u"
    if 'digits' in keys:
        _charset += "?d"
    if 'special' in keys:
        _charset += "?s"

    return _charset

def parse_dictionaries(keys: list):
    _dictionaries = []
    for key in keys:
        if ".txt" in key:
            _dictionaries.append(key)

    return _dictionaries