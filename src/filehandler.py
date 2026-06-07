"""
@author: Irfan Kurniawan
"""

from pathlib import Path

from .server import *
from .login import *


class FileHandler:
    def __init__(self) -> None:
        pass

    # fungsi untuk menyimpan data server ke dalam file txt
    def save_server(self):
        fs = FungsiServer()

        with open("data/server.txt", "w") as f:
            for i in fs.server_list:
                data = f"{i.nama}|{i.id}|{i.ip}|{i.status}\n"
                f.write(data)

    # fungsi untuk mengambil data dari file txt
    def load_server(self):
        server_list = []
        try:
            with open(Path("data/server.txt"), "r") as f:
                for baris in f:
                    data = baris.strip().split(
                        "|"
                    )  # ini untuk mengubah text menjadi sebuah data dalam list
                    nama = data[0]
                    id = data[1]
                    ip = data[2]
                    status = data[3]

                    obj = ServerNode(nama, id, ip, status)  # data kembali menjadi objek
                    server_list.append(obj)
            return server_list
        except:
            print("File Tidak Ditemukan")
            return

    # fungsi untuk menyimpan data akun ke dalam file json
    def save_akun(self):
        l = Login()
        with open("data/dalam-json/akun.json", "w") as f:
            json.dump(l.servers, f, indent=4)

    # fungsi untuk mengambil data dari file json
    def load_akun(self):
        l = Login()
        try:
            with open("data/dalam-json/akun.json", "r") as f:
                return json.load(f)
        except:
            print("File Tidak Ditemukan")
            return

    # fungsi untuk menyimpan log stack
    def save_log(self, log_stack):
        with open("data/log.txt", "w") as f:
            for log in log_stack:
                f.write(log + "\n")

    # fungsi untuk mengambil data dari file log.txt
    def load_log(self):
        log_stack = []
        try:
            with open("data/log.txt", "r") as f:
                for baris in f:
                    log_stack.append(baris.strip())
            return log_stack
        except:
            print("File Tidak Ditemukan")

    # fungsi untuk menyimpan data packet
    def save_packet(self, packet_queue):
        with open("data/packet.txt", "w") as f:
            for packet in packet_queue:
                f.write(packet + "\n")

    # fungsi untuk mengambil data dari file packet.txt
    def load_packet(self):
        packet_queue = []
        try:
            with open("data/packet.txt", "r") as f:
                for baris in f:
                    packet_queue.append(baris.strip())
            return packet_queue
        except:
            print("File Tidak Ditemukan")

    # fungsi untuk menyimpan file json
    def save_json(self, path: str, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # fungsi untuk memuat file json
    def load_json(self, path: str | Path) -> dict | list:
        with open(path, "r") as f:
            return json.load(f)

    def save_all(self):
        self.save_server()
        self.save_akun()
        # self.save_log()
        # self.save_packet()

        print("[ALL DATA SAVED]")


if __name__ == "__main__":
    fh = FileHandler()
    fh.save_all()
