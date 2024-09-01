# import subprocess
# import os

# path = "hashcat/hashcat.exe"

# hashcat_version = subprocess.Popen(["hashcat/hashcat.exe", "--help"], stdout=subprocess.PIPE, cwd=os.path.dirname(path))

# print(hashcat_version.communicate())

# # result = subprocess.run(["hashcat/hashcat.exe", "--help"], capture_output=True, text=True)
# # print(result.stdout)



# https://medium.com/@ekiser_48014/python-penetration-testing-using-hashcat-and-python-to-crack-windows-passwords-34cb4f052bf3
# Tool that simplifies the Hashcat cracking process.

# import subprocess

# word_list_file = "..\wordlists\\10k-most-common.txt"
# hash_type = "MD5"
# hash_mode = "0"
# output_file = "..\output.txt"
# hash_file = "..\hash.txt"

# # Prompt for type of hash
# hash_type = input("Enter the type of hash (e.g., NTLM, SHA1, SHA256, MD5): ")

# # Create a dictionary to map hash type to hashcat mode
# hash_modes = {
#     'NTLM': '1000',
#     'SHA1': '100',
#     'SHA256': '1400',
#     'MD5': '0'
# }

# # Check if entered hash type is valid
# if hash_type.upper() not in hash_modes:
#     print("Invalid hash type. Supported hash types are: NTLM, SHA1, SHA256, and MD5.")
#     exit()

# # Get the hash mode from the dictionary
# hash_mode = hash_modes[hash_type.upper()]

# # Prompt for location of hash file
# hash_file = input("Enter the location of the hash file: ")

# # Prompt for location to save findings
# output_file = input("Enter the location to save the findings: ")

# # Prompt for location of word list file
# word_list_file = input("Enter the location of the word list file: ")

# # Define hashcat command with multithreading option
# hashcat_command = f".\hashcat.exe -m {hash_mode} -a 0 {hash_file} {word_list_file} -o {output_file}"

# # Execute hashcat command using subprocess
# try:
#     output = subprocess.check_output(hashcat_command, shell=True, cwd = r"C:\Users\Admin\Documents\PK SEMESTR 3\PRACA MAGISTERSKA\DISTRIBUTED CRACKING\hashcat")
#     print(output.decode("utf-8"))
# except subprocess.CalledProcessError as e:
#     print(f"Error executing hashcat command: {e}")

# def divide_string_oneliner(s, n):
#     return [s[i:i+n] for i in range(0, len(s), n)]
# # Example usage
# result = divide_string_oneliner("abcdefghijkl", 5)
# print(result)

class Solution:
    def solve(self, s, n):
        i=0
        f=[]
        while(i<len(s)):
            f.append(s[i:i+n])
            i+=n
        return(f)
ob = Solution()
print(ob.solve("abcdefghijkl", int(len("abcdefghijkl")/8)))