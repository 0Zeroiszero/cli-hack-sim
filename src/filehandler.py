"""Modul filehandler untuk aplikasi CLI Hack Sim.

Menyediakan kelas FileHandler untuk menyimpan dan memuat
data server, akun, log, packet, dan file JSON.

@author: Irfan Kurniawan
"""

import json
from pathlib import Path

from .server import ServerNode


class FileHandler:
    """Kelas untuk menangani operasi baca/tulis file.

    Menyediakan metode untuk menyimpan dan memuat data server,
    akun, log aktivitas, packet, serta file JSON umum.
    """

    def __init__(self) -> None:
        """Inisialisasi objek FileHandler."""
        pass

    # def save_server(self) -> None:
    #     """Menyimpan data server ke dalam file teks.
    #
    #     Menulis data server dari FungsiServer ke file data/server.txt
    #     dengan format: nama|id|ip|status per baris.
    #     """
    #     fs = FungsiServer()
    #
    #     with open("data/server.txt", "w") as f:
    #         for i in fs.server_list:
    #             data = f"{i.nama}|{i.id}|{i.ip}|{i.status}\n"
    #             f.write(data)

    def load_server(self) -> list[ServerNode] | None:
        """Memuat data server dari file teks.

        Membaca file data/server.txt dan mengembalikan daftar
        objek ServerNode.

        Returns:
            list[ServerNode] | None: Daftar objek ServerNode,
                atau None jika file tidak ditemukan.
        """
        server_list = []
        try:
            with open(Path("data/server.txt")) as f:
                for baris in f:
                    data = baris.strip().split(
                        "|"
                    )  # ini untuk mengubah text menjadi sebuah data dalam list
                    nama = data[0]
                    id = data[1]
                    ip = data[2]
                    status = data[3]

                    obj = ServerNode(
                        nama, id, ip, status
                    )  # data kembali menjadi objek
                    server_list.append(obj)
            return server_list
        except Exception:
            print("File Tidak Ditemukan")
            return None

    # def save_akun(self) -> None:
    #     """Menyimpan data akun ke dalam file JSON.
    #
    #     Menulis data akun dari Login ke file
    #     data/dalam-json/akun.json.
    #     """
    #     l = Login()
    #     with open("data/dalam-json/akun.json", "w") as f:
    #         json.dump(l.servers, f, indent=4)

    # def load_akun(self) -> dict | None:
    #     """Memuat data akun dari file JSON.
    #
    #     Returns:
    #         dict | None: Data akun dalam bentuk dictionary,
    #             atau None jika file tidak ditemukan.
    #     """
    #     l = Login()
    #     try:
    #         with open("data/dalam-json/akun.json", "r") as f:
    #             return json.load(f)
    #     except Exception:
    #         print("File Tidak Ditemukan")
    #         return None

    # def save_log(self, log_stack: list[str]) -> None:
    #     """Menyimpan log stack ke dalam file teks.
    #
    #     Args:
    #         log_stack: Daftar string log yang akan disimpan.
    #     """
    #     with open("data/log.txt", "w") as f:
    #         for log in log_stack:
    #             f.write(log + "\n")

    # def load_log(self) -> list[str] | None:
    #     """Memuat data log dari file teks.
    #
    #     Returns:
    #         list[str] | None: Daftar string log,
    #             atau None jika file tidak ditemukan.
    #     """
    #     log_stack = []
    #     try:
    #         with open("data/log.txt", "r") as f:
    #             for baris in f:
    #                 log_stack.append(baris.strip())
    #         return log_stack
    #     except Exception:
    #         print("File Tidak Ditemukan")
    #         return None

    # def save_packet(self, packet_queue: list[str]) -> None:
    #     """Menyimpan packet queue ke dalam file teks.
    #
    #     Args:
    #         packet_queue: Daftar string packet yang akan disimpan.
    #     """
    #     with open("data/packet.txt", "w") as f:
    #         for packet in packet_queue:
    #             f.write(packet + "\n")

    # def load_packet(self) -> list[str] | None:
    #     """Memuat data packet dari file teks.
    #
    #     Returns:
    #         list[str] | None: Daftar string packet,
    #             atau None jika file tidak ditemukan.
    #     """
    #     packet_queue = []
    #     try:
    #         with open("data/packet.txt", "r") as f:
    #             for baris in f:
    #                 packet_queue.append(baris.strip())
    #         return packet_queue
    #     except Exception:
    #         print("File Tidak Ditemukan")
    #         return None

    # def save_json(self, path: str, data: dict | list) -> None:
    #     """Menyimpan data ke dalam file JSON.
    #
    #     Args:
    #         path: Path file tujuan.
    #         data: Data yang akan disimpan (dict atau list).
    #     """
    #     with open(path, "w", encoding="utf-8") as f:
    #         json.dump(data, f, indent=4, ensure_ascii=False)

    def load_json(self, path: str | Path) -> dict | list:
        """Memuat data dari file JSON.

        Args:
            path: Path file JSON yang akan dibaca.

        Returns:
            dict | list: Data yang dimuat dari file JSON.
        """
        with open(path) as f:
            return json.load(f)

    # def save_all(self) -> None:
    #     """Menyimpan seluruh data (server dan akun) ke file.
    #
    #     Memanggil save_server() dan save_akun() untuk menyimpan
    #     semua data terkini ke dalam file masing-masing.
    #     """
    #     self.save_server()
    #     self.save_akun()
    #     # self.save_log()
    #     # self.save_packet()
    #
    #     print("[ALL DATA SAVED]")


if __name__ == "__main__":
    fh = FileHandler()
    # fh.save_all()
    pass
