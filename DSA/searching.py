"""Modul pencarian server berdasarkan alamat IP.

Menyediakan fungsi binary search dan linear search untuk mencari
server dalam file data/server.txt berdasarkan alamat IPv4.

@author: Irfan Kurniawan
"""

from ipaddress import AddressValueError, IPv4Address
from pathlib import Path


def cari_server_binary(
    target: str,
) -> list[tuple[int, str, str, str, str, bool]] | bool:
    """Mencari server berdasarkan IP menggunakan binary search.

    Data server dibaca dari file data/server.txt, kemudian diurutkan
    berdasarkan nilai numerik IP sebelum dilakukan pencarian biner.

    Args:
        target: Alamat IPv4 dalam bentuk string (contoh: "192.168.1.90").

    Returns:
        list[tuple] jika pencarian berhasil atau gagal ditemukan,
        berupa daftar tuple (index, ip, server_id, server_name, status, found).
        False jika alamat IP target tidak valid (AddressValueError).

    """
    try:
        target_int = int(IPv4Address(target))
        data: list[list[str]] = []
        data_cari: list[tuple[int, str, str, str, str, bool]] = []

        with open(Path("data/server.txt")) as f:
            for line in f:
                data.append(line.strip().split("|"))

        data_copy = data[:]

        for item in data_copy:
            bentuk_angka = int(IPv4Address(item[2]))
            item[2] = str(bentuk_angka)

        data_copy.sort(key=lambda x: int(x[2]))

        left = 0
        right = len(data_copy) - 1
        idx = 0
        ketemu = False

        while left <= right:
            mid = (left + right) // 2
            kembali_ip = str(IPv4Address(int(data_copy[mid][2])))

            if int(data_copy[mid][2]) == target_int:
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

            if int(data_copy[mid][2]) < target_int:
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


def cari_server_linear(
    target: IPv4Address,
) -> list[tuple[int, str, str, str, str, bool]]:
    """Mencari server berdasarkan IP menggunakan linear search.

    Data server dibaca dari file data/server.txt, kemudian dilakukan
    pencarian secara berurutan dari indeks pertama hingga terakhir.

    Args:
        target: Alamat IPv4 dalam bentuk IPv4Address.

    Returns:
        list[tuple] berisi daftar tuple
        (index, ip, server_id, server_name, status, found).

    """
    data: list[list[str]] = []
    data_cari: list[tuple[int, str, str, str, str, bool]] = []
    ketemu = False

    with open(Path("data/server.txt")) as f:
        for line in f:
            data.append(line.strip().split("|"))

    for indeks, item in enumerate(data):
        ip = IPv4Address(item[2])

        if ip > target:
            data_cari.append(
                (indeks, item[2], item[1], item[0], item[3], ketemu)
            )
            break

        if ip == target:
            ketemu = True
            data_cari.append(
                (indeks, item[2], item[1], item[0], item[3], ketemu)
            )
            break
        else:
            data_cari.append(
                (indeks, item[2], item[1], item[0], item[3], ketemu)
            )
    return data_cari


if __name__ == "__main__":
    from pprint import pprint

    pprint(cari_server_binary("192.168.1.90"))
    pprint(cari_server_linear(IPv4Address("192.168.1.40")))
