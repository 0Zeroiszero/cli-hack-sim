import sys
import os
from pathlib import Path

def scan_credential_access():
    file_path = Path("src/data/dalam-json/akun_dan_status_server.json")
    with open(file_path, "r") as file:
        data = file.read()
    dict = {
        "rows": [data.servers for data in data['servers']]
    }
    for idx, row in enumerate(dict['rows'], start=0):
        index = idx + 1
        dict['rows'][idx]['index'] = index
        if dict['rows'][idx]['status'] == "UNLOCKED":
            data.append('is_unlocked', True)
        else:            
            data.append('is_unlocked', False)
            forbidden_characters = '*'
            locked_username = forbidden_characters.replace(char for char in dict['rows'][idx]['username'])
            locked_password = forbidden_characters.replace(char for char in dict['rows'][idx]['password'])
            dict['rows'][idx]['username'] = locked_username
            dict['rows'][idx]['password'] = locked_password
    dict['summary'] = {
        "total_servers": len(dict['rows']),
        "unlocked_servers": sum(1 for row in dict['rows'] if row['status'] == "UNLOCKED"),
        "locked_servers": sum(1 for row in dict['rows'] if row['status'] == "LOCKED")
    }
    dict['summary']['scan_result'] = f"{dict['summary']['unlocked_servers']} credential dapat dilihat"
    return dict
