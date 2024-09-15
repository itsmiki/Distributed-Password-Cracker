import configparser
import subprocess 
from config import HashcatConfig, GeneralConfig
import re
from accessify import private
import typing as t
from utlis import HashType
from colorama import Fore, Style
    

class HashcatInterface():
    def __init__(self, config: configparser.SectionProxy, general_config: configparser.SectionProxy) -> None:
        self.config = config
        self.general_config = general_config

    def benchmark(self, hash_type: int = 0) -> str:
        hashcat_command = f"{self.general_config['runCommandPrefix']}{self.config['binaryName']} -b -m {hash_type}"
        try:
            output = subprocess.check_output(hashcat_command, shell=True, cwd = self.config['binaryDir'])
            return re.search(r'Speed.#\*\.\.\.\.\.\.\.\.\.:\ \ (.*?)\n', output.decode('utf-8')).group(1)
        except subprocess.CalledProcessError as e:
            print(f"Error executing hashcat command: {e}")

    def dictionary_attack(self, hash_type: HashType, hash_file: str, output_file: str, wordlist_file: str) -> str:
        hashcat_command = f"{self.general_config['runCommandPrefix']}{self.config['binaryName']} -m {hash_type} -a 0 {self.config['tempDir']}{hash_file} {self.config['wordlistDir']}{wordlist_file} -o {self.config['tempDir']}{output_file}"
        
        hash_cracked = self.check_if_found_before(hashcat_command)
        if  hash_cracked is not None:
            return hash_cracked
        
        return self.run_command(hashcat_command) # output_file
    
    def bruteforce_attack(self, hash_type: HashType, hash_file: str, output_file: str, charset: list, pattern: str) -> str:
        hashcat_command = f"{self.general_config['runCommandPrefix']}{self.config['binaryName']} -m {hash_type} -a 3 {self.config['tempDir']}{hash_file} -1 '{charset[0]}' -2 '{charset[1]}' '{pattern}' -o {self.config['tempDir']}{output_file}"
        
        hash_cracked = self.check_if_found_before(hashcat_command)
        if  hash_cracked is not None:
            return hash_cracked
        
        return self.run_command(hashcat_command) # output_file
    
    def mask_attack(self, hash_type: HashType, hash_file: str, output_file: str, wordlist_file: str, mask_file: str) -> str:
        hashcat_command = f"{self.general_config['runCommandPrefix']}{self.config['binaryName']} -m {hash_type} -a 0 {self.config['tempDir']}{hash_file} {self.config['wordlistDir']}{wordlist_file} -r {self.config['tempDir']}{mask_file} -o {self.config['tempDir']}{output_file}"
        
        hash_cracked = self.check_if_found_before(hashcat_command)
        if  hash_cracked is not None:
            return hash_cracked
        
        return self.run_command(hashcat_command) # output_file
        
    @private
    def run_command(self, command) -> t.Optional[str]:
        try:
            output = subprocess.check_output(command, shell=True, cwd = self.config['binaryDir'])
            print(Fore.GREEN + Style.BRIGHT + "Hash was found!")
            return output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            # print(f"Error executing hashcat command: {e}")
            print(Fore.YELLOW + Style.BRIGHT +"Hash not found during this task...")

    @private
    def check_if_found_before(self, command) -> t.Optional[str]:
        output = subprocess.check_output(f"{command} --show", shell=True, cwd = self.config['binaryDir'])
        if len(output) < 1:
            return None
        return output.decode('utf-8')
    


if __name__ == "__main__":
    hashcat = HashcatInterface(HashcatConfig("config.ini").get_config(), GeneralConfig("config.ini").get_config())
    # print(hashcat.benchmark())
    # print(hashcat.dictionary_attack(HashType.MD5.value, "..\\temp\\hash.txt", "..\\temp\\output.txt", "10k-most-common.txt"))
    print(hashcat.bruteforce_attack(HashType.MD5.value, "..\\temp\\hash.txt", "..\\temp\\output.txt", "?l?u?d?s", "?1?1?1?1?1 --increment"))



