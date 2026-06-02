import sys
import os
from pathlib import Path
import json

akun_dan_status_server_path = Path("src/data/dalam-json/akun_dan_status_server.json")
brute_force = Path("src/data/dalam-json/bruteforce.json")

return_dict = []
# format_tuple = ("index", "server_profile", "username", "password", "status", "found")

def brute_force_attack():
    with open(akun_dan_status_server_path, "r") as file:
        akun_dan_status_server = json.load(file)
    
    for idx, item in enumerate(akun_dan_status_server.get("servers", [])):
        server_id = item.get("server_id")
        server_name = item.get("server_name")
        username = item.get("username")
        password = item.get("password")
        status = item.get("status")
    

    server_profile =  (server_id, server_name)

    with open(brute_force, "r") as file:
        brute_force_data = json.load(file)
    
    for entry in brute_force_data.get("brute_force_attempts", []):
        index = entry.get("index")
        username = entry.get("username")
        password = entry.get("password")
        
    # Cek apakah kombinasi username dan password cocok dengan data akun_dan_status_server
        found = False
        for item in akun_dan_status_server.get("servers", []):
            if (server_profile == (item.get("server_id"), item.get("server_name")) and
                item.get("username") == username and
                item.get("password") == password):
                found = True
                break

        
        return_dict.append((index, server_profile, username, password, status, found))
    
    return return_dict
