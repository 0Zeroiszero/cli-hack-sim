"""
@author: Abdullah Affandi
"""

import time
import subprocess
import os
from pathlib import Path
from ipaddress import IPv4Address, AddressValueError

# Implementasi dari questionary.select()
from utils import (
    make_menu_selection_question,
    tampilkan_bandwidth_progress,
    display_search_ip_result,
)

from DSA import TrafficQueue
from DSA import LogAktivitas
from DSA import SortingServer
from DSA import cari_server_binary, cari_server_linear
from .filehandler import FileHandler

from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.prompt import Confirm

from rich_pyfiglet import RichFiglet


# TODO: BUTUH MENAMBAHKAN USERNAME DI SAMPING LOG-NYA
class MainMenu:
    def __init__(self):
        self.console = Console()
        self.traffic = TrafficQueue("src/data/dalam-json/traffic.json")
        self.log_aktivitas = LogAktivitas()

    def clear_screen(self):
        command = "cls" if os.name == "nt" else "clear"
        subprocess.run(command, shell=True)

    def intro(self):
        try:
            self.log_aktivitas.add_log("Inisialisasi aplikasi", value=1)

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
        except KeyboardInterrupt:
            pass

    def header_menu(
        self,
        menu: str,
        sub_menu: str,
        *,
        operator: str = "OPERATOR",
        access: str = "NO ACCESS",
        choosen_server: str = None,
    ):
        self.clear_screen()

        # Memastikan setiap kata diawali huruf kapital dan sisanya lower
        lokasi_rapi = " ".join(word.capitalize() for word in sub_menu.split())

        header = Panel(
            Text("HACKER NETWORK SIMULATION", justify="center", style="white"),
            border_style="green",
            title=f"{menu.upper()} - {sub_menu.upper()}",
            title_align="center",
        )

        info_text = Text()
        info_text.append(f"Menu Saat ini : {lokasi_rapi}\n", style="bold green")
        info_text.append("Aktivitas     : ", style="bold green")
        info_text.append_text(self.log_aktivitas.peek())

        info = Group(
            info_text,
            "\n",
            f"Operator      : {operator}\nAccess        : {access}\nServer        : {choosen_server}",
        )

        self.layout = Group(header, "\n", info, "\n")
        self.console.print(
            self.layout, Rule(style="white", characters="="), style="bold green"
        )

    def main_menu(self):
        self.log_aktivitas.add_log("Masuk ke Beranda")
        self.clear_screen()

        self.header_menu("Main Menu", "Beranda")

        choice = make_menu_selection_question(
            question=[
                "Kelola Server",
                "Network & Route",
                "Traffic Queue",
                "Struktur Data",
                "Keluar",
            ],
            value=[1, 2, 3, 4, 0],
        ).ask()

        if choice == 0:
            with self.console.status("[bold red]Exiting..."):
                time.sleep(0.5)
                self.clear_screen()
                return

        self.sub_menu(choice)

    def sub_menu(self, menu_id: int):
        """
        [1] Kelola Server
        [2] Network & Route
        [3] Traffic Queue
        [4] Struktur Data
        [0] Keluar

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
    def kelola_server_menu(self):
        "[1] Kelola Server"
        self.log_aktivitas.add_log("Masuk ke Kelola Server")
        self.clear_screen()

        self.header_menu("MENU", "Kelola Server")

        choice = make_menu_selection_question(
            question=[
                "Pilih / Tampilkan Server",
                "Cari Server Berdasarkan IP",
                "Urutkan Server Berdasarkan Bandwidth",
                "Monitoring Server Circular",
                "Kembali ke Beranda",
            ],
            value=[1, 2, 3, 4, 0],
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

    # TODO: [1.1] "Pilih / Tampilkan Server"
    def pilih_tampilkan_server(self):
        '''[1.1] "Pilih / Tampilkan Server"'''
        self.log_aktivitas.add_log("Masuk ke Tampilkan Server")
        pass

    # TODO: [1.2] "Cari Server Berdasarkan IP"
    def cari_server_berdasarkan_ip_server(self):
        '''[1.2] "Cari Server Berdasarkan IP"'''
        self.log_aktivitas.add_log("Masuk ke Cari Server Berdasarkan IP")
        self.clear_screen()

        self.header_menu("SUB MENU", "Cari Server Berdasarkan IP")

        choice = make_menu_selection_question(
            question=[
                "Cari Menggunakan Binary Search",
                "Cari Menggunakan Linear Search",
                "Batalkan",
            ],
            value=[1, 2, 0],
        ).ask()

        match choice:
            case 1:
                self.log_aktivitas.add_log("Mencari IP Secara Binary", value=2)
                self.clear_screen()

                self.header_menu("SUB MENU", "Cari Server Berdasarkan IP")

                input_ip = self.console.input("Masukkan IP Server: ")

                try:
                    hasil_binary = cari_server_binary(IPv4Address(input_ip))
                except AddressValueError:
                    hasil_binary = False

                if not hasil_binary:
                    self.console.input("Tidak valid, masukkan ulang...")
                    self.cari_server_berdasarkan_ip_server()
                elif hasil_binary:
                    panel_binary = display_search_ip_result(result=hasil_binary)
                    self.console.print(panel_binary)

                    self.console.input(
                        "\nTekan Enter untuk kembali ke menu pencarian..."
                    )
                    self.cari_server_berdasarkan_ip_server()
            case 2:
                self.log_aktivitas.add_log("Mencari IP Secara Linear", value=2)
                self.clear_screen()

                self.header_menu("SUB MENU", "Cari Server Berdasarkan IP")

                input_ip = self.console.input("Masukkan IP Server: ")

                try:
                    hasil_linear = cari_server_linear(IPv4Address(input_ip))
                except AddressValueError:
                    hasil_linear = False

                if not hasil_linear:
                    self.console.input("Tidak valid, masukkan ulang...")
                    self.cari_server_berdasarkan_ip_server()
                elif hasil_linear:
                    panel_linier = display_search_ip_result(result=hasil_linear)
                    self.console.print(panel_linier)

                    self.console.input(
                        "\nTekan Enter untuk kembali ke menu pencarian..."
                    )
                    self.cari_server_berdasarkan_ip_server()
            case 0:
                # [1] Kelola Server
                self.kelola_server_menu()

    # TODO: [1.3] "Urutkan Server Berdasarkan Bandwidth"
    def urutkan_server_berdasarkan_bandwidth_server(self):
        '''[1.3] "Urutkan Server Berdasarkan Bandwidth"'''
        self.log_aktivitas.add_log("Mengurutkan Server Berdasarkan Bandwidth", value=2)
        self.clear_screen()
        self.console.clear()

        self.header_menu("SUB MENU", "Pilih / Tampilkan Server")

        bandwidth_server = []
        bandwidth_file_data = FileHandler().load_json(
            Path("src/data/dalam-json/akun_dan_status_server.json")
        )

        idx = 0
        for req in bandwidth_file_data["servers"]:
            bandwidth_server.append(
                [idx, req["server_id"], req["server_name"], req["bandwidth_mbps"]]
            )
            idx += 1

        self.console.print(tampilkan_bandwidth_progress(data=bandwidth_server))

        choice = Confirm.ask("Jalankan pengurutan?", console=self.console, default=True)

        if choice:
            sorted_server = SortingServer().urutkan_server()

            with self.console.status("[bold yellow]Mengurutkan server...") as status:
                time.sleep(1)
                status.update("[bold green]Server terurut...")
                time.sleep(1)

            self.console.print(
                tampilkan_bandwidth_progress(data=sorted_server, rank=True)
            )
            self.console.input("\nTekan Enter untuk kembali ke menu...")

            self.kelola_server_menu()
        else:
            self.kelola_server_menu()

    # TODO: [1.4] "Monitoring Server Circular"
    def monitoring_server_circular_server(self):
        '''[1.4] "Monitoring Server Circular"'''
        self.log_aktivitas.add_log("Masuk ke Monitoring Server Circular")
        pass

    # [2] Network & Route
    def network_route_menu(self):
        "[2] Network & Route"
        self.log_aktivitas.add_log("Masuk ke Network & Route")
        self.clear_screen()

        self.header_menu("MENU", "Network & Route")

        choice = make_menu_selection_question(
            question=[
                "Tampilkan Topologi Jaringan",
                "Cari Rute Tercepat",
                "Kembali ke Beranda",
            ],
            value=[1, 2, 0],
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

    # TODO: [2.1] "Tampilkan Topologi Jaringan"
    def tampilkan_topologi_jaringan(self):
        '''[2.1] "Tampilkan Topologi Jaringan"'''
        self.log_aktivitas.add_log("Masuk ke Tampilkan Topologi Jaringan")
        pass

    # TODO: [2.2] "Cari Rute Tercepat"
    def cari_rute_tercepat_jaringan(self):
        '''[2.2] "Cari Rute Tercepat"'''
        self.log_aktivitas.add_log("Masuk ke Cari Rute Tercepat")
        pass

    # TODO: [3] Traffic Queue
    def traffic_queue_menu(self):
        """[3] Traffic Queue"""
        self.log_aktivitas.add_log("Masuk ke Traffic Queue")
        self.clear_screen()

        self.header_menu(
            "MENU",
            "Traffic Queue",
            operator="ADMIN SELURUH SERVER",
            access="ALL RESOURCE",
            choosen_server="@owner",
        )

        # TODO: Butuh penambahan traffic setiap keluar menu ini buat simulasi
        # TODO: Kayaknya dimasukkan ke tomporary file dulu dan di save pas exit dari CLI
        # self.traffic.refresh_traffic()

        self.console.print(
            f"Queue Size: {self.traffic.size()}", end="\n\n", style="bold yellow"
        )

        choice = make_menu_selection_question(
            question=[
                "Tampilkan Queue Traffic",
                "Kelola Traffic",
                "Kembali ke Beranda",
            ],
            value=[1, 2, 0],
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

    # TODO: [3.1] "Tampilkan Queue Traffic"
    def tampilkan_queue_traffic(self):
        '''[3.1] "Tampilkan Queue Traffic"'''
        self.log_aktivitas.add_log("Masuk ke Tampilkan Queue Traffic")
        self.log_aktivitas.add_log("Menampilkan Queue Traffic", value=2)
        self.header_menu(
            "SUB MENU",
            "Tampilkan Queue Traffic",
            operator="ADMIN SELURUH SERVER",
            access="ALL RESOURCE",
            choosen_server="@owner",
        )
        self.traffic.display()

        choice = make_menu_selection_question(
            question=["Kembali ke Traffic Queue"],
            value=[0],
        ).ask()

        match choice:
            case 0:
                self.traffic_queue_menu()

    # TODO: [3.2] "Kelola Traffic"
    def kelola_traffic(self):
        '''[3.2] "Kelola Traffic"'''
        self.log_aktivitas.add_log("Masuk ke Kelola Traffic")
        self.clear_screen()

        self.header_menu(
            "SUB MENU",
            "Kelola Traffic",
            operator="ADMIN SELURUH SERVER",
            access="ALL RESOURCE",
            choosen_server="@owner",
        )

        choice = make_menu_selection_question(
            question=[
                "Lihat Traffic Terdepan",
                "Proses Traffic Terdepan",
                "Kembali ke Traffic Queue",
            ],
            value=[1, 2, 0],
        ).ask()

        match choice:
            case 1:
                # Handle "Lihat Traffic Terdepan"
                self.lihat_traffic_terdepan_traffic()
            case 2:
                # Handle "Proses Traffic Terdepan"
                self.proses_traffic_terdepan_traffic()
            case 0:
                # naik ke [3] Traffic Queue
                self.traffic_queue_menu()

    # TODO: [3.2.1] "Lihat Traffic Terdepan"
    def lihat_traffic_terdepan_traffic(self):
        '''[3.2.1] "Lihat Traffic Terdepan"'''
        self.log_aktivitas.add_log("Masuk ke Lihat Traffic Terdepan")
        self.log_aktivitas.add_log("Melihat Traffic Terdepan", value=2)
        self.header_menu(
            "SUB MENU",
            "Lihat Traffic Terdepan",
            operator="ADMIN SELURUH SERVER",
            access="ALL RESOURCE",
            choosen_server="@owner",
        )
        self.traffic.display_front()

        choice = make_menu_selection_question(
            question=["Kembali ke Kelola Traffic"],
            value=[0],
        ).ask()

        match choice:
            case 0:
                self.kelola_traffic()

    # TODO: [3.2.2] "Proses Traffic Terdepan"
    def proses_traffic_terdepan_traffic(self):
        '''[3.2.2] "Proses Traffic Terdepan"'''
        self.log_aktivitas.add_log("Masuk ke Proses Traffic Terdepan")
        self.log_aktivitas.add_log("Memproses Traffic Terdepan", value=2)
        self.header_menu(
            "SUB MENU",
            "Proses Traffic Terdepan",
            operator="ADMIN SELURUH SERVER",
            access="ALL RESOURCE",
            choosen_server="@owner",
        )
        self.traffic.display_dequeue()

        choice = make_menu_selection_question(
            question=["Kembali ke Kelola Traffic"],
            value=[0],
        ).ask()

        match choice:
            case 0:
                self.kelola_traffic()

    # TODO: [4] Struktur Data
    def struktur_data_menu(self):
        """[4] Struktur Data"""
        self.log_aktivitas.add_log("Masuk ke Struktur Data")
        self.clear_screen()

        self.header_menu("MENU", "Struktur Data")

        choice = make_menu_selection_question(
            question=[
                "Tampilkan Folder Server",
                "Kelola Stack Log Aktivitas",
                "Kembali ke Beranda",
            ],
            value=[1, 2, 0],
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

    # TODO: [4.1] "Tampilkan Folder Server"
    def tampilkan_folder_server_data(self):
        '''[4.1] "Tampilkan Folder Server"'''
        self.log_aktivitas.add_log("Masuk ke Tampilkan Folder Server")
        pass

    # TODO: [4.2] "Kelola Stack Log Aktivitas"
    def kelola_stack_log_aktivitas_data(self):
        '''[4.2] "Kelola Stack Log Aktivitas"'''

        self.log_aktivitas.add_log("Masuk ke Kelola Stack Log Aktivitas")
        self.clear_screen()

        self.header_menu("SUB MENU", "Struktur Data")
        self.log_aktivitas.show_logs()

        choice = make_menu_selection_question(
            question=[
                "Hapus log teratas",
                "Hapus seluruh log",
                "Kembali ke Struktur Data",
            ],
            value=[1, 2, 0],
        ).ask()

        self.clear_screen()

        match choice:
            case 1:
                self.header_menu("SUB MENU", "Struktur Data")
                self.log_aktivitas.pop()
                self.log_aktivitas.show_logs()

                self.console.print(
                    "\n[bold yellow]Log teratas berhasil dihapus. Kembali ke menu Struktur Data...[/bold yellow]"
                )
                time.sleep(2)
                self.struktur_data_menu()

            case 2:
                self.header_menu("SUB MENU", "Struktur Data")
                self.log_aktivitas.clear_log()
                self.log_aktivitas.show_logs()

                self.console.print(
                    "\n[bold yellow]Seluruh log berhasil dihapus. Kembali ke menu Struktur Data...[/bold yellow]"
                )
                time.sleep(2)
                self.struktur_data_menu()

            case 0 | None:
                self.struktur_data_menu()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.intro()
    main_menu.main_menu()
