"""
@author: Abdullah Affandi
"""

from importlib.resources import path
import time
import datetime
import subprocess
import os
import sys
import json
from pathlib import Path


import questionary
from questionary import Style

from rich.console import Console, Group
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich_pyfiglet import RichFiglet

from src.filehandler import FileHandler


<<<<<<< HEAD
class MainMenu:
    """Menu utama aplikasi CLI Hack Sim dengan navigasi berbasis questionary.

    Menyediakan menu berjenjang untuk mengelola server, network,
    traffic queue, dan struktur data.
    """

    def __init__(self) -> None:
        """Inisialisasi MainMenu dengan console dan style questionary."""
=======

class MainMenu:
    def __init__(self):
>>>>>>> main
        self.console = Console()
        self.questionary_style = Style(
            [
                ("qmark", "fg:#00ff00 bold"),
                ("question", "fg:#ffffff bold"),
                ("answer", "fg:#00ff00 italic"),
                ("pointer", "fg:#00ff00 bold"),
                ("highlighted", "fg:#000000 bg:#00ff00 bold"),
                ("selected", "fg:#ff0033 bold"),
                ("separator", "fg:#333333"),
                ("instruction", "fg:#00aa00 italic"),
                ("text", "fg:#00ff00"),
                ("disabled", "fg:#444444 italic"),
            ]
        )

<<<<<<< HEAD
    def clear_screen(self) -> None:
        """Membersihkan layar terminal."""
        command = "cls" if os.name == "nt" else "clear"
        subprocess.run(command, shell=True)

    def intro(self) -> None:
        """Menampilkan animasi intro CLI Hack Sim dengan RichFiglet."""
=======
    def clear_screen(self):
        command = "cls" if os.name == "nt" else "clear"
        subprocess.run(command, shell=True)

    def intro(self):
>>>>>>> main
        self.clear_screen()
        self.intro_text = RichFiglet(
            text="CLI Hack Sim",
            font="ansi_shadow",
            justify="center",
            colors=["#006400", "#90EE90", "#FFFFFF"],
            fps=4,
            timer=2,
            remove_blank_lines=True,
            dev_console=self.console,
            animation="gradient_down",
        )
        self.console.print(self.intro_text)
        self.console.print()

        # TODO: Tambahkan yang perlu diinisialisasi di sini
        with self.console.status("[bold green]Initializing..."):
            time.sleep(1.5)

<<<<<<< HEAD
    def header_menu(self, menu: str, sub_menu: str) -> None:
        """Menampilkan header menu dengan panel, informasi waktu, dan operator.

        Args:
            menu: Nama menu utama (misal "Main Menu").
            sub_menu: Nama sub-menu saat ini (misal "Beranda").
        """
=======
    def header_menu(self, menu: str, sub_menu: str):
>>>>>>> main
        self.clear_screen()

        # Memastikan setiap kata diawali huruf kapital dan sisanya lower
        lokasi_rapi = " ".join(word.capitalize() for word in sub_menu.split())

        header = Panel(
            Text("HACKER NETWORK SIMULATION", justify="center", style="white"),
            border_style="green",
            title=f"{menu.upper()} - {sub_menu.upper()}",
            title_align="center",
        )

        col = Columns(
            [
                Text(
                    f"Menu Saat ini : {lokasi_rapi}\n"
                    f"Waktu         : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    style="bold green",
                ),
                Text(
                    "Operator      : UNKNOWN\nAccess        : NO ACCESS",
                    style="bold green",
                ),
            ],
            equal=True,
            expand=True,
        )

        self.layout = Group(header, "\n", col, "\n")

        self.console.print(
            self.layout,
            Rule(style="white", characters="="),
            style="bold green",
        )

<<<<<<< HEAD
    def main_menu(self) -> None:
        """Menampilkan menu utama dan menangani pilihan pengguna."""
=======
    def main_menu(self):
>>>>>>> main
        self.clear_screen()

        self.header_menu("Main Menu", "Beranda")

        choice = questionary.select(
            "Pilih Menu:",
            qmark="",
            choices=[
                questionary.Choice("Kelola Server", value=1, shortcut_key="1"),
<<<<<<< HEAD
                questionary.Choice(
                    "Network & Route", value=2, shortcut_key="2"
                ),
=======
                questionary.Choice("Network & Route", value=2, shortcut_key="2"),
>>>>>>> main
                questionary.Choice("Traffic Queue", value=3, shortcut_key="3"),
                questionary.Choice("Struktur Data", value=4, shortcut_key="4"),
                questionary.Choice("Keluar", value=0, shortcut_key="0"),
            ],
            default=0,
            use_shortcuts=True,
            style=self.questionary_style,
            instruction="Gnakan arrow keys atau angka",
        ).ask()

        if choice == 0:
            with self.console.status("[bold red]Exiting..."):
                time.sleep(0.5)

        self.sub_menu(choice)

<<<<<<< HEAD
    def sub_menu(self, menu_id: int) -> None:
        """Mengarahkan ke sub-menu berdasarkan pilihan menu_id.

        Args:
            menu_id: ID menu yang dipilih (1=Kelola Server, 2=Network & Route,
                     3=Traffic Queue, 4=Struktur Data, 0=Keluar).
=======
    def sub_menu(self, menu_id: int):
        """
        [1] Kelola Server
        [2] Network & Route
        [3] Traffic Queue
        [4] Struktur Data
        [0] Keluar

>>>>>>> main
        """
        self.clear_screen()

        match menu_id:
            case 1:
                self.kelola_server_menu()
            case 2:
                self.network_route_menu()
                pass
            case 3:
                self.traffic_queue_menu()
                pass
            case 4:
                self.struktur_data_menu()

    # [1] Kelola Server
<<<<<<< HEAD
    def kelola_server_menu(self) -> None:
        """[1] Menampilkan sub-menu Kelola Server."""
=======
    def kelola_server_menu(self):
        "[1] Kelola Server"
>>>>>>> main
        self.clear_screen()

        self.header_menu("SUB MENU", "Kelola Server")

        choice = questionary.select(
            "Pilih Menu:",
            qmark="",
            choices=[
                questionary.Choice(
                    "Pilih / Tampilkan Server", value=1, shortcut_key="1"
                ),
                questionary.Choice(
                    "Cari Server Berdasarkan IP", value=2, shortcut_key="2"
                ),
                questionary.Choice(
<<<<<<< HEAD
                    "Urutkan Server Berdasarkan Bandwidth",
                    value=3,
                    shortcut_key="3",
=======
                    "Urutkan Server Berdasarkan Bandwidth", value=3, shortcut_key="3"
>>>>>>> main
                ),
                questionary.Choice(
                    "Monitoring Server Circular", value=4, shortcut_key="4"
                ),
<<<<<<< HEAD
                questionary.Choice(
                    "Kembali ke Menu Utama", value=0, shortcut_key="0"
                ),
=======
                questionary.Choice("Kembali ke Menu Utama", value=0, shortcut_key="0"),
>>>>>>> main
            ],
            default=0,
            use_shortcuts=True,
            style=self.questionary_style,
            instruction="Gnakan arrow keys atau angka",
        ).ask()

        match choice:
            case 1:
                # Handle "Pilih / Tampilkan Server"
                self.pilih_tampilkan_server()
            case 2:
                # Handle "Cari Server Berdasarkan IP"
                self.cari_server_berdasarkan_ip_server()
            case 3:
                # Handle "Urutkan Server Berdasarkan Bandwidth"
                self.urutkan_server_berdasarkan_bandwidth_server()
            case 4:
                # Handle "Monitoring Server Circular"
                self.monitoring_server_circular_server()
            case 0:
                self.main_menu()

    # [1.1] "Pilih / Tampilkan Server"
    def pilih_tampilkan_server(self):
        '''[1.1] "Pilih / Tampilkan Server"'''
        folder_path = Path("D:\kuliah\cli-hack-sim\src\data\dalam-json")
        server_files = list(folder_path.glob("*.json"))
        if not server_files:
<<<<<<< HEAD
            self.console.print(
                "Tidak ada server yang tersedia.", style="bold red"
            )
            time.sleep(1.5)
            return
        server_choices = [
            questionary.Choice(file.stem, value=file.stem)
            for file in server_files
=======
            self.console.print("Tidak ada server yang tersedia.", style="bold red")
            time.sleep(1.5)
            return
        server_choices = [
            questionary.Choice(file.stem, value=file.stem) for file in server_files
>>>>>>> main
        ]
        server_choices.append(questionary.Choice("Kembali", value="back"))
        choice = questionary.select(
            "Pilih Server:",
            qmark="",
            choices=server_choices,
        ).ask()

        if choice == "back":
            self.kelola_server_menu()
        else:
            self.tampilkan_isi_server(choice)

    # [1.2] "Cari Server Berdasarkan IP"
    def cari_server_berdasarkan_ip_server(self):
        '''[1.2] "Cari Server Berdasarkan IP"'''
        pass

    # [1.3] "Urutkan Server Berdasarkan Bandwidth"
    def urutkan_server_berdasarkan_bandwidth_server(self):
        '''[1.3] "Urutkan Server Berdasarkan Bandwidth"'''
        folder_path = Path("D:\kuliah\cli-hack-sim\src\data\dalam-json")
        server_files = list(folder_path.glob("*.json"))
        if not server_files:
<<<<<<< HEAD
            self.console.print(
                "Tidak ada server yang tersedia.", style="bold red"
            )
=======
            self.console.print("Tidak ada server yang tersedia.", style="bold red")
>>>>>>> main
            time.sleep(1.5)
            return
        servers = []
        for file in server_files:
            with open(file, "r") as f:
                data = json.load(f)
                servers.append((file.stem, data.get("bandwidth", 0)))
        servers.sort(key=lambda x: x[1], reverse=True)
        self.console.print(
            "Server diurutkan berdasarkan bandwidth (terbesar ke terkecil):",
            style="bold green",
        )
        for name, bandwidth in servers:
            self.console.print(f"{name}: {bandwidth}")

    # [1.4] "Monitoring Server Circular"
    def monitoring_server_circular_server(self):
        '''[1.4] "Monitoring Server Circular"'''
        pass

    # [2] Network & Route
<<<<<<< HEAD
    def network_route_menu(self) -> None:
        """[2] Menampilkan sub-menu Network & Route."""
=======
    def network_route_menu(self):
        "[2] Network & Route"
>>>>>>> main
        self.clear_screen()

        self.header_menu("SUB MENU", "Network & Route")

        choice = questionary.select(
            "Pilih Menu:",
            qmark="",
            choices=[
                questionary.Choice(
                    "Tampilkan Topologi Jaringan", value=1, shortcut_key="1"
                ),
<<<<<<< HEAD
                questionary.Choice(
                    "Cari Rute Tercepat", value=2, shortcut_key="2"
                ),
                questionary.Choice(
                    "Kembali ke Menu Utama", value=0, shortcut_key="0"
                ),
=======
                questionary.Choice("Cari Rute Tercepat", value=2, shortcut_key="2"),
                questionary.Choice("Kembali ke Menu Utama", value=0, shortcut_key="0"),
>>>>>>> main
            ],
            default=0,
            use_shortcuts=True,
            style=self.questionary_style,
            instruction="Gnakan arrow keys atau angka",
        ).ask()

        match choice:
            case 1:
                # Handle "Tampilkan Topologi Jaringan"
                self.tampilkan_topologi_jaringan()
            case 2:
                # Handle "Cari Rute Tercepat"
                self.cari_rute_tercepat_jaringan()
            case 0:
                self.main_menu()

    # [2.1] "Tampilkan Topologi Jaringan"
    def tampilkan_topologi_jaringan(self):
        '''[2.1] "Tampilkan Topologi Jaringan"'''

    # [2.2] "Cari Rute Tercepat"
    def cari_rute_tercepat_jaringan(self):
        '''[2.2] "Cari Rute Tercepat"'''
        pass

    # [3] Traffic Queue
    def traffic_queue_menu(self):
        """[3] Traffic Queue"""
        self.clear_screen()

        self.header_menu("SUB MENU", "Traffic Queue")

        # TODO: Ganti dengan ukuran antrian yang sebenarnya
        self.console.print("Queue Size: N", end="\n\n", style="bold yellow")

        choice = questionary.select(
            "Pilih Menu:",
            qmark="",
            choices=[
                questionary.Choice(
                    "Tampilkan Queue Traffic", value=1, shortcut_key="1"
                ),
<<<<<<< HEAD
                questionary.Choice(
                    "Kelola Traffic", value=2, shortcut_key="2"
                ),
                questionary.Choice(
                    "Kembali ke Menu Utama", value=0, shortcut_key="0"
                ),
=======
                questionary.Choice("Kelola Traffic", value=2, shortcut_key="2"),
                questionary.Choice("Kembali ke Menu Utama", value=0, shortcut_key="0"),
>>>>>>> main
            ],
            default=0,
            use_shortcuts=True,
            style=self.questionary_style,
            instruction="Gnakan arrow keys atau angka",
        ).ask()

        match choice:
            case 1:
                # Handle "Tampilkan Queue Traffic"
                self.tampilkan_queue_traffic()
            case 2:
                # Handle "Kelola Traffic"
                self.kelola_traffic()
            case 0:
                self.main_menu()

    # [3.1] "Tampilkan Queue Traffic"
    def tampilkan_queue_traffic(self):
        '''[3.1] "Tampilkan Queue Traffic"'''
        pass

    def kelola_traffic(self):
        '''[3.2] "Kelola Traffic"'''
        self.clear_screen()

        self.header_menu("SUB MENU", "Kelola Traffic")

        choice = questionary.select(
            "Pilih Menu:",
            qmark="",
            choices=[
<<<<<<< HEAD
                questionary.Choice(
                    "Lihat Traffic Terdepan", value=1, shortcut_key="1"
                ),
                questionary.Choice(
                    "Proses Traffic Terdepan", value=2, shortcut_key="2"
                ),
                questionary.Choice(
                    "Kembali ke Menu Utama", value=0, shortcut_key="0"
                ),
=======
                questionary.Choice("Lihat Traffic Terdepan", value=1, shortcut_key="1"),
                questionary.Choice(
                    "Proses Traffic Terdepan", value=2, shortcut_key="2"
                ),
                questionary.Choice("Kembali ke Menu Utama", value=0, shortcut_key="0"),
>>>>>>> main
            ],
            default=0,
            use_shortcuts=True,
            style=self.questionary_style,
            instruction="Gnakan arrow keys atau angka",
        ).ask()

        match choice:
            case 1:
                # Handle "Tampilkan Queue Traffic"
                pass
            case 2:
                # Handle "Proses Traffic Terdepan"
                pass
            case 0:
                # naik ke [3] Traffic Queue
                self.traffic_queue_menu()

    # [4] Struktur Data
    def struktur_data_menu(self):
        """[4] Struktur Data"""
        self.clear_screen()

        self.header_menu("SUB MENU", "Struktur Data")

        choice = questionary.select(
            "Pilih Menu:",
            qmark="",
            choices=[
                questionary.Choice(
                    "Tampilkan Folder Server", value=1, shortcut_key="1"
                ),
                questionary.Choice(
                    "Kelola Stack Log Aktivitas", value=2, shortcut_key="2"
                ),
<<<<<<< HEAD
                questionary.Choice(
                    "Kembali ke Menu Utama", value=0, shortcut_key="0"
                ),
=======
                questionary.Choice("Kembali ke Menu Utama", value=0, shortcut_key="0"),
>>>>>>> main
            ],
            default=0,
            use_shortcuts=True,
            style=self.questionary_style,
            instruction="Gnakan arrow keys atau angka",
        ).ask()

        match choice:
            case 1:
                # Handle "Tampilkan Folder Server"
                self.tampilkan_folder_server_data()
            case 2:
                # Handle "Kelola Stack Log Aktivitas"
                self.kelola_stack_log_aktivitas_data()
            case 0:
                self.main_menu()

    # [4.1] "Tampilkan Folder Server"
    def tampilkan_folder_server_data(self):
<<<<<<< HEAD
        """[4.1] Menampilkan daftar folder server dari file JSON."""
        self.clear_screen()

        self.header_menu("SUB MENU", "Folder Server")
        file_path = Path(
            "..\..\src\data\dalam-json\daftar_folder_file_server.json"
        )
        if not file_path.exists():
            self.console.print(
                "File daftar_folder_file_server.json tidak ditemukan.",
                style="bold red",
            )
            time.sleep(1.5)
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        self.console.print("Daftar Folder Server:", style="bold green")
=======
<<<<<<< HEAD
        self.clear_screen()

        self.header_menu("SUB MENU", "Folder Server")
        file_path = Path("..\..\src\data\dalam-json\daftar_folder_file_server.json")
        if not file_path.exists():
            self.console.print("File daftar_folder_file_server.json tidak ditemukan.", style="bold red")
=======
        FileHandler().load_json("daftar_folder_file_server.json")
        folder_data = FileHandler().get_data("daftar_folder_file_server.json")
        if not folder_data:
            self.console.print(
                "Tidak ada data folder server yang tersedia.", style="bold red"
            )
>>>>>>> d9fb384b3aa07da4687279f7d54ae9a3fc84fa1c
            time.sleep(1.5)
            return
        
        with open(file_path, "r") as f:
            data = json.load(f)
        
        self.console.print("Daftar Folder Server:", style="bold green")
<<<<<<< HEAD
>>>>>>> main
        for idx, servers in enumerate(data, start=1):
            is_last = idx == len(data) - 1
            connector = "└── " if is_last else "├── "
            print(f"{sys.prefix}{connector}{idx}. {servers['server_name']}")
            for folder in servers["folders"]:
                extension = "    " if is_last else "│   "
                print(f"{sys.prefix}{extension}{folder}")
                if folder.is_dict():
                    for file in folder["files"]:
                        print(f"{sys.prefix}{extension}{file}")
<<<<<<< HEAD
=======
=======
        for idx, folder in enumerate(folder_data, start=1):
            self.console.print(
                f"{idx}. {folder['server_name']}, content: {folder['contents']}"
            )
>>>>>>> d9fb384b3aa07da4687279f7d54ae9a3fc84fa1c
>>>>>>> main

    # [4.2] "Kelola Stack Log Aktivitas"
    def kelola_stack_log_aktivitas_data(self):
        '''[4.2] "Kelola Stack Log Aktivitas"'''
        pass


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.intro()
    main_menu.main_menu()
