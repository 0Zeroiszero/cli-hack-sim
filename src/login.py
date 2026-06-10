"""Modul login untuk aplikasi CLI Hack Sim.

Menyediakan fungsionalitas login sederhana menggunakan
pendekatan dictionary untuk validasi kredensial.
"""


<<<<<<< HEAD
=======

>>>>>>> main
class Login:
    """Kelas untuk menangani proses login pengguna.

    Attributes:
        servers: Data server yang dimuat dari file JSON.
    """

    def __init__(self) -> None:
        """Inisialisasi objek Login."""
        pass

<<<<<<< HEAD
=======
    # def login_user(self, servers: dict) -> None:
    #     """Melakukan login pengguna berdasarkan data server.
    #
    #     Args:
    #         servers: Dictionary data server yang berisi daftar server
    #             beserta kredensialnya.
    #
    #     """
    #     akun = [item['credential'] for item in servers['servers']]
    #
    #     username = input('Username: ')
    #     password = input('Password: ')
    #
    #     for i in akun:
    #         if username == i['username']:
    #             print ('\nLogin Berhasil!') if password == i['password'] else print('\nPassword Salah!')
    #             break
    #     else:
    #         print('\nUsername Tidak Ditemukan!')

>>>>>>> main

if __name__ == "__main__":
    l = Login()
