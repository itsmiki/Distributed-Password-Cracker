from enum import Enum

class HashType(Enum):
    MD5 = 0
    SHA1 = 100
    SHA2_256 = 1400
    SHA2_512 = 1700
    SHA3_256 = 17400
    SHA3_512 = 17600

class AttackType(Enum):
    dictionary = 1
    bruteforce = 2
    mask = 3

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

def print_dict(task: dict) -> None:
    for key in task:
        print(f"{key}: {task[key]}")

def move_terminal(lines: int) -> None:
    for _line in range (0, lines):
        print("\n")

    print("\033[%dA" % (lines))
