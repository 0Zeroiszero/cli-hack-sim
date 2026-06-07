"""Modul utama untuk menjalankan aplikasi CLI Hack Sim.

Modul ini merupakan titik masuk utama aplikasi. Ketika dijalankan,
aplikasi akan menampilkan intro dan menu utama.
"""

from src.main_menu import MainMenu


def main() -> None:
    """Menjalankan aplikasi CLI Hack Sim.

    Membuat instance MainMenu, menampilkan animasi intro,
    lalu masuk ke menu utama.
    """
    main_menu = MainMenu()
    main_menu.intro()
    main_menu.main_menu()


if __name__ == "__main__":
    main()
