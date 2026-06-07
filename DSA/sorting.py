"""Modul pengurutan server berdasarkan bandwidth.

Menyediakan kelas SortingServer yang mengurutkan daftar server
berdasarkan bandwidth (Mbps) menggunakan algoritma bubble sort.

@author: Irfan Kurniawan
"""

import json
from pathlib import Path


class SortingServer:
    """Mengurutkan server berdasarkan bandwidth menggunakan bubble sort.

    Attributes:
        urutan: Daftar sementara server sebelum diurutkan.
        urutan_data: Daftar server yang sudah diurutkan.

    """

    def __init__(self) -> None:
        """Inisialisasi atribut pengurutan."""
        self.urutan: list[list[int | str]] = []
        self.urutan_data: list[tuple[int, str, str, int]] = []

    def urutkan_server(self) -> list[tuple[int, str, str, int]]:
        """Mengurutkan server berdasarkan bandwidth tertinggi (bubble sort).

        Membaca data server dari file JSON, kemudian mengurutkan
        secara menurun berdasarkan bandwidth_mbps.

        Returns:
            list[tuple] berisi (index, server_id, server_name, bandwidth_mbps)
            yang sudah diurutkan dari bandwidth tertinggi ke terendah.

        """
        with open(
            Path("data/dalam-json/akun_dan_status_server.json")
        ) as f:
            data = json.load(f)

        idx = 0
        for req in data["servers"]:
            self.urutan.append(
                [
                    idx,
                    req["server_id"],
                    req["server_name"],
                    req["bandwidth_mbps"],
                ]
            )
            idx += 1

        n = len(self.urutan)

        for i in range(n - 1):
            swap = False
            for j in range(n - i - 1):
                if self.urutan[j][3] < self.urutan[j + 1][3]:
                    self.urutan[j], self.urutan[j + 1] = (
                        self.urutan[j + 1],
                        self.urutan[j],
                    )
                    self.urutan[j][0], self.urutan[j + 1][0] = (
                        self.urutan[j + 1][0],
                        self.urutan[j][0],
                    )
                    swap = True
            if not swap:
                break

        for i in self.urutan:
            self.urutan_data.append(tuple(i))

        return self.urutan_data


if __name__ == "__main__":
    ss = SortingServer()
    from pprint import pprint

    pprint(ss.urutkan_server())
