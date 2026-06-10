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

    def check_duplicate_ip(self, data: dict) -> bool:
        """Memeriksa apakah ada duplikat IP dalam data server.

        Args:
            data: Data server yang dimuat dari file JSON.

        Returns:
            bool: True jika ditemukan IP duplikat, False jika tidak.
        """
        ips = [server["ip"] for server in data["servers"]]
        return len(ips) != len(set(ips))

    def load_json(self, path: str | Path) -> dict | list:
        """Memuat data dari file JSON.

        Args:
            path: Path file JSON yang akan dibaca.

        Returns:
            dict | list: Data yang dimuat dari file JSON.
        """
        with open(path) as f:
            return json.load(f)


if __name__ == "__main__":
    fh = FileHandler()
    pass
