 
# # import csv 
# import csv 
  
# # open input CSV file as source 
# # open output CSV file as result 
# with open(r"C:\Users\Admin\Downloads\10millionPasswords\10millionPasswords.txt", "r") as source: 
#     reader = csv.reader(source) 
      
#     with open("10millionPasswords.txt", "w") as result: 
#         for r in reader: 
#             # print(r[1])
#             # Use CSV Index to remove a column from CSV 
#             #r[3] = r["year"] 
#             result.write((r[1] + "\n"))



# import OS module
# import os
# # Get the list of all files and directories
# path = r"C:\Users\Admin\Documents\PK SEMESTR 3\PRACA MAGISTERSKA\DISTRIBUTED CRACKING\client\hashcat\rules"
# dir_list = os.listdir(path)
# print("Files and directories in "", path, "" :")
# # prints all files
# print(dir_list)
# config = {}

# dir_list.remove("hybrid")

# for dir in dir_list:
#     with open(f"{path}\{dir}", "r", encoding="utf8") as f:
#         config[dir] = len(f.readlines())


# print(config)

# import OS module
import os
# Get the list of all files and directories
path = r"C:\Users\Admin\Documents\PK SEMESTR 3\PRACA MAGISTERSKA\DISTRIBUTED CRACKING\client\wordlists"
dir_list = os.listdir(path)
print("Files and directories in "", path, "" :")
# prints all files
print(dir_list)
config = {}

# dir_list.remove("hybrid")

for dir in dir_list:
    with open(f"{path}\{dir}", "r", encoding="utf8") as f:
        config[dir] = len(f.readlines())


print(config)
