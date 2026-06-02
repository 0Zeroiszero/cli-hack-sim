import sys
import os
from pathlib import Path
import json

akun_dan_status_server_path = Path("src/data/dalam-json/akun_dan_status_server.json")
brute_force = Path("src/data/dalam-json/bruteforce.json")

return_dict = []

def brute_force_attack():
    with open(akun_dan_status_server_path, "r") as file:
        akun_dan_status_server = json.load(file)
    
    for idx, item in enumerate(akun_dan_status_server.get("servers", [])):
        server_id = item.get("server_id")
        server_name = item.get("server_name")
        username = item.get("username")
        password = item.get("password")
        status = item.get("status")
        info = (idx, server_id, server_name, username, password, status, False)
        return_dict.append(info)


    for username, password in brute_force.read_text_file():
        username = username.strip()
        password = password.strip()

    for item in return_dict:
        if item[3] == username and item[4] == password:
            return_dict[return_dict.index(item)] = (*item[:-1], True)
            break
        

    return return_dict
