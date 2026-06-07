"""@author: Alif Akbar; @modified: Abdullah Affandi

Fungsi bruteforce login untuk membuka akses server."""

from pathlib import Path

from src.filehandler import FileHandler


def bruteforce_server(server_id):
    """Melakukan bruteforce login terhadap server berdasarkan server_id.

    Membaca data kredensial dari file JSON, menggunakan hash table untuk
    pencocokan cepat, dan mengembalikan hasil (atau None jika gagal).

    Args:
        server_id: Target server ID, contoh: "SRV002".

    Returns:
        dict jika ditemukan kecocokan:
            {
                "server_id": str,
                "server_name": str,
                "access": "UNLOCKED",
                "username": str,
                "password": str,
            }
        None jika tidak ada kecocokan.
    """
    akun_data = FileHandler().load_json(
        Path("src/data/dalam-json/akun_dan_status_server.json"),
    )
    brute_data = FileHandler().load_json(
        Path("src/data/dalam-json/bruteforce.json"),
    )

    # Cari server target berdasarkan server_id
    target_server = None
    for server in akun_data.get("servers", []):
        if server["server_id"] == server_id:
            target_server = server
            break

    if target_server is None:
        return None

    original_username = target_server["credential"]["username"]
    original_password = target_server["credential"]["password"]

    # Bangun hash table dari data bruteforce
    # Key: "username:password" -> O(1) lookup
    brute_hash = {}
    for entry in brute_data:
        key = f"{entry['username']}:{entry['password']}"
        brute_hash[key] = entry

    # Cari kredensial asli dalam hash table
    target_key = f"{original_username}:{original_password}"
    if target_key in brute_hash:
        return {
            "server_id": server_id,
            "server_name": target_server["server_name"],
            "access": "UNLOCKED",
            "username": original_username,
            "password": original_password,
        }

    return None

if __name__ == "__main__":
    from pprint import pprint
    
    bf = bruteforce_server("SRV001")
    pprint(bf)