import sys
import os
from pathlib import Path
import json


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = [(key, value)]
        else:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    self.table[index][i] = (key, value)
                    return
            self.table[index].append((key, value))

    def search(self, key):
        index = self._hash(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        return None

    def delete(self, key):
        index = self._hash(key)
        if self.table[index] is not None:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    del self.table[index][i]
                    return True
        return False

    def __str__(self):
        return str([bucket for bucket in self.table if bucket is not None])
    
    def brute_force_attack(self):
        akun_dan_status_server_path = Path("src/data/dalam-json/akun_dan_status_server.json")
        brute_force = Path("src/data/dalam-json/bruteforce.json")
        return_dict = []

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
