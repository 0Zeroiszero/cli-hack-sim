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

<<<<<<< HEAD

if __name__ == "__main__":
    fs = FungsiServer()
=======
    # def tampilkan_server(self, data: list[ServerNode]) -> None:
    #     """Menampilkan daftar server dalam format tabel.
    #
    #     Args:
    #         data: Daftar objek ServerNode yang akan ditampilkan.
    #
    #     """
    #     print("\n+========================================+")
    #     print("|             SERVER MONITOR             |")
    #     print("+========================================+")
    #     for i in data:
    #         print(f" Server ID         : {i.nama}")
    #         print(f" Server Name       : {i.id}")
    #         print(f" IP Address        : {i.ip}")
    #         print(f" Status            : {i.status}\n")
    #     print("+========================================+")


# def cek_access_server() -> dict:
#     """Memeriksa status akses seluruh server.
#
#     Membaca data server dari file JSON dan mengembalikan ringkasan
#     status akses (UNLOCKED/LOCKED) beserta kredensial.
#
#     Returns:
#         dict: Dictionary berisi daftar baris server dan ringkasan.
#             Struktur:
#             {
#                 "rows": list[dict],
#                 "summary": {
#                     "total_server": int,
#                     "unlocked_access": int,
#                     "locked_access": int,
#                     "visible_credential": int,
#                 }
#             }
#     """
#     file_path = Path("data/dalam-json/akun_dan_status_server.json")
#
#     with open(file_path, "r") as file:
#         data = json.load(file)
#
#     hasil = {
#         "rows": [],
#         "summary": {
#             "total_server": 0,
#             "unlocked_access": 0,
#             "locked_access": 0,
#             "visible_credential": 0,
#         }
#     }
#
#     for indeks, req in enumerate(data['servers']):
#         access = req["access"]
#         credential = req["credential"]
#
#         if access == "UNLOCKED":
#             username = credential["username"]
#             password = credential["password"]
#             is_unlocked = True
#
#             hasil["summary"]["unlocked_access"] += 1
#             hasil["summary"]["visible_credential"] += 1
#         else:
#             username = "********"
#             password = "********"
#             is_unlocked = False
#
#             hasil["summary"]["locked_access"] += 1
#
#         row = {
#             "indeks": indeks,
#             "server_id": req["server_id"],
#             "server_name": req["server_name"],
#             "access": access,
#             "username": username,
#             "password": password,
#             "is_unlocked": is_unlocked,
#         }
#
#         hasil["rows"].append(row)
#         hasil["summary"]["total_server"] = len(data["servers"])
#
#     return hasil


# def get_server_detail(server_id: str) -> dict:
#     """Mendapatkan detail server berdasarkan server_id.
#
#     Args:
#         server_id: ID server yang ingin dicari (contoh: "SRV002").
#
#     Returns:
#         dict: Dictionary berisi detail server termasuk kredensial
#             (jika akses UNLOCKED) atau pesan error jika tidak ditemukan.
#     """
#     file_path = Path("data/dalam-json/akun_dan_status_server.json")
#
#     with open(file_path, "r") as file:
#         data = json.load(file)
#
#     for req in data["servers"]:
#         if server_id == req["server_id"]:
#             if req["access"] == "UNLOCKED":
#                 hasil = {
#                     "server_id": req["server_id"],
#                     "server_name": req["server_name"],
#                     "ip": req["ip"],
#                     "bandwidth_mbps": req["bandwidth_mbps"],
#                     "status": req["status"],
#                     "access": req['access'],
#                     "vulnerable": req["vulnerable"],
#                     "credential": {
#                         "username": req["credential"]['username'],
#                         "password": req["credential"]['password'],
#                         "is_visible": True
#                     },
#                     "security_note": (
#                         "Credential dapat ditampilkan karena access server sudah UNLOCKED. "
#                     )
#                 }
#                 return hasil
#             else:
#                 hasil = {
#                     "server_id": req["server_id"],
#                     "server_name": req["server_name"],
#                     "ip": req["ip"],
#                     "bandwidth_mbps": req["bandwidth_mbps"],
#                     "status": req["status"],
#                     "access": req['access'],
#                     "vulnerable": req["vulnerable"],
#                     "credential": {
#                         "username": "*******",
#                         "password": "*******",
#                         "is_visible": False
#                     },
#                     "security_note": (
#                         "Credential disembunyikan karena access LOCKED. "
#                         "Gunakan fitur login/unlock untuk membuka akses. "
#                     )
#                 }
#                 return hasil
#     return {
#         "error": True,
#         "message": f"Server dengan ID '{server_id}' tidak ditemukan. "
#     }


if __name__ == "__main__":
    fs = FungsiServer()
    # fs.tambah_server()
    # fs.tampilkan_server(data=fs.server_list)
    # from pprint import pprint
    # pprint(get_server_detail("SRV002"))
>>>>>>> main
    pass
