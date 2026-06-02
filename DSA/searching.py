"""
@author: Irfan Kurniawan
@modified: 01/06/2026 13.26 WIB oleh Abdullah Affandi
- Menambahkan try...except pada binary search AddressValueError
- Konversi IPv4Address as str
@modified: 02/06/2026 10.48 WIB oleh Abdullah Affandi
- Menambahkan komentar pada fungsi cari_server_linear untuk menjelaskan rentang pencarian linier
@modified: 02/06/2026 17.00 WIB oleh Abdullah Affandi
- perbaiki logika perbandingan IP pada fungsi cari_server_linear
"""

from pathlib import Path
from ipaddress import IPv4Address, AddressValueError


# fungsi mencari server berdasarkan ip menggunakan binary search
def cari_server_binary(target: str):
    try:
        target = int(IPv4Address(target))
        data = []
        data_cari = []

        with open(Path("src/data/server.txt"), "r") as f:
            for line in f:
                data.append(line.strip().split("|"))

        data_copy = data[:]

        for item in data_copy:
            bentuk_angka = int(IPv4Address(item[2]))
            item[2] = bentuk_angka

        data_copy.sort(key=lambda x: x[2])

        left = 0
        right = len(data_copy) - 1
        idx = 0
        ketemu = False

        while left <= right:
            mid = (left + right) // 2
            kembali_ip = str(IPv4Address(data_copy[mid][2]))

            if data_copy[mid][2] == target:
                ketemu = True
                data_cari.append(
                    (
                        idx,
                        kembali_ip,
                        data_copy[mid][1],
                        data_copy[mid][0],
                        data_copy[mid][3],
                        ketemu,
                    )
                )
                return data_cari

            if data_copy[mid][2] < target:
                left = mid + 1
            else:
                right = mid - 1

            data_cari.append(
                (
                    idx,
                    kembali_ip,
                    data_copy[mid][1],
                    data_copy[mid][0],
                    data_copy[mid][3],
                    ketemu,
                )
            )
            idx += 1

        return data_cari
    except AddressValueError:
        return False


# fungsi mencari server berdasarkan ip menggunakan linear search
def cari_server_linear(target: IPv4Address):
    data = []
    data_cari = []
    ketemu = False

    with open(Path("src/data/server.txt"), "r") as f:
        for line in f:
            data.append(line.strip().split("|"))

    for indeks, item in enumerate(data):
        ip = IPv4Address(item[2])
        # Untuk mendapatkan rentang pencarian linier,
        # kita bisa membandingkan nilai IP yang sedang diperiksa dengan target.
        # item[2] >= target
        # Misal IP yang dicari 192.168.1.12
        # Namun rentang IP yang dikembalikan 192.168.1.10 - 192.168.1.20

        if ip > target:
            data_cari.append((indeks, item[2], item[1], item[0], item[3], ketemu))
            break

        if ip == target:
            ketemu = True
            data_cari.append((indeks, item[2], item[1], item[0], item[3], ketemu))
            break
        else:
            data_cari.append((indeks, item[2], item[1], item[0], item[3], ketemu))
    return data_cari


if __name__ == "__main__":
    # ss = SearchingServer()
    from pprint import pprint

    pprint(cari_server_binary("192.168.1.90"))
    pprint(cari_server_linear("192.168.1.40"))
