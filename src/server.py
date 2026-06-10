"""Modul server untuk aplikasi CLI Hack Sim.

Berisi kelas ServerNode, FungsiServer, serta fungsi utilitas
untuk mengelola data server dan akses kredensial.

@author: Irfan Kurniawan
@modified: 02/06/2026 21.40 WIB oleh Abdullah Affandi
- Mengganti path lokasi akun_dan_status_server.json pada fungsi tambah_server
- Menghilangkan print pada fungsi tambah_server karena sudah tidak diperlukan
"""

import json
import random


class ServerNode:
    """Mewakili node/server dalam jaringan.

    Attributes:
        id: ID unik server (contoh: "SRV001").
        nama: Nama server.
        ip: Alamat IP server.
        status: Status server (ONLINE, OFFLINE, dll).
    """

    def __init__(self, nama: str, id: str, ip: str, status: str) -> None:
        """Inisialisasi node server.

        Args:
            nama: Nama server.
            id: ID unik server.
            ip: Alamat IP server.
            status: Status server.
        """
        self.id: str = id
        self.nama: str = nama
        self.ip: str = ip
        self.status: str = status


class FungsiServer:
    """Kelas untuk mengelola operasi terkait server.

    Attributes:
        server_list: Daftar objek ServerNode.
        ip_unik: Set alamat IP unik.
        koordinat_server: Dictionary koordinat server.
        network: Dictionary representasi jaringan.
    """

    def __init__(self) -> None:
        """Inisialisasi objek FungsiServer."""
        self.server_list: list[ServerNode] = []
        self.ip_unik: set[str] = set()
        self.koordinat_server: dict[str, tuple[int, int]] = {}
        self.network: dict[str, list] = {}

    def tambah_server(self) -> None:
        """Menambahkan server dari file JSON ke dalam daftar server.

        Membaca data server dari file akun_dan_status_server.json,
        lalu membuat objek ServerNode untuk setiap entri server.
        """
        with open("data/dalam-json/akun_dan_status_server.json") as f:
            data = json.load(f)

        nama_server = [item["server_name"] for item in data["servers"]]
        server_id = [item["server_id"] for item in data["servers"]]
        ip_server = [item["ip"] for item in data["servers"]]
        status_server = [item["status"] for item in data["servers"]]

        for i in range(len(nama_server)):
            nama = nama_server[i]
            id = server_id[i]
            ip = ip_server[i]
            status = status_server[i]

            if ip_server[i] in self.ip_unik:
                print("IP sudah digunakan")
                return

            self.ip_unik.add(ip_server[i])

            posisi = ((random.randint(1, 100)), (random.randint(1, 100)))

            self.koordinat_server[nama_server[i]] = posisi
            self.network[nama_server[i]] = []

            server = ServerNode(nama, id, ip, status)
            self.server_list.append(server)


if __name__ == "__main__":
    fs = FungsiServer()
    pass
