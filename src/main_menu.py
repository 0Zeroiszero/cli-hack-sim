"""Modul main menu untuk aplikasi CLI Hack Sim.

@author: Abdullah Affandi
"""

import os
import re
import subprocess
import time
from ipaddress import AddressValueError, IPv4Address
from pathlib import Path

from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Confirm
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich_pyfiglet import RichFiglet

from DSA import (
    CircularServerNode,
    LogAktivitas,
    ServerCarousel,
    ServerTreeBuilder,
    SortingServer,
    TrafficQueue,
    cari_server_binary,
    cari_server_linear,
    inorder,
    postorder,
    preorder,
)
from DSA.graph.graph import Graph
from utils import (
    ask_for_ip,
    ask_for_server,
    bruteforce_server,
    display_search_ip_result,
    make_menu_selection_question,
    make_traversal_folder,
    tampilkan_bandwidth_progress,
)

from .filehandler import FileHandler
from .server import ServerNode  # noqa: TC001

# ── Constants ────────────────────────────────────────────────────────────

TRAVERSAL_PREORDER = 1
TRAVERSAL_INORDER = 2
TRAVERSAL_POSTORDER = 3


class MainMenu:
    """Pengontrol menu utama untuk aplikasi CLI Hack Sim."""

    def __init__(self) -> None:
        """Inisialisasi atribut dan dependensi utama."""
        self._console = Console()
        self._traffic = TrafficQueue("data/dalam-json/traffic.json")
        self._log_aktivitas = LogAktivitas()
        self._node_from_server: ServerNode | None = None
        self._server_id: str | None = None
        if self._node_from_server is not None:
            self._server_id = self._node_from_server.id
        self._server_carousel = ServerCarousel(self._server_id)
        self._operator = "Operator"
        self._server_data: dict = FileHandler().load_json(
            Path("data/dalam-json/akun_dan_status_server.json"),
        )
        self._circular_server = CircularServerNode(self._server_data)

    @property
    def _choosen_server(self) -> str:
        """Mengembalikan nama server yang sedang dipilih.

        Returns:
            str: Nama server atau 'No Server Selected' jika belum ada.

        """
        if self._node_from_server:
            return self._node_from_server.nama
        return "No Server Selected"

    @property
    def _access_server(self) -> str:
        """Mengembalikan status akses server yang dipilih.

        Returns:
            str: 'UNLOCKED' jika server dapat diakses, 'LOCKED' jika tidak
                 atau 'No Access' jika server tidak ditemukan.

        """
        if self._node_from_server is None:
            return "No Access"
        for server in self._server_data["servers"]:
            if server["server_id"] == self._node_from_server.id:
                return (
                    "UNLOCKED" if server["access"] == "UNLOCKED" else "LOCKED"
                )
        return "No Access"

    # ── Utility ──────────────────────────────────────────────────────────────

    def _clear_screen(self) -> None:
        """Membersihkan layar terminal."""
        command = "cls" if os.name == "nt" else "clear"
        subprocess.run(command, shell=True, check=False)  # noqa: S602

    def intro(self) -> None:
        """Menampilkan animasi intro dan urutan inisialisasi."""
        try:
            self._log_aktivitas.add_log("Inisialisasi aplikasi", value=1)
            self._clear_screen()
            self._intro_text = RichFiglet(
                text="CLI Hack Sim",
                font="ansi_shadow",
                justify="center",
                colors=["#006400", "#90EE90", "#FFFFFF"],
                fps=4,
                timer=2,
                remove_blank_lines=True,
                dev_console=self._console,
                animation="gradient_down",
            )
            self._console.print(self._intro_text)
            self._console.print()
            with self._console.status("[bold green]Initializing..."):
                time.sleep(1.5)
        except KeyboardInterrupt:
            pass

    def _header_menu(self, menu: str, sub_menu: str) -> None:
        """Menampilkan panel header untuk menu dan sub-menu tertentu.

        Args:
            menu: Nama menu utama.
            sub_menu: Nama sub-menu yang sedang aktif.

        """
        self._clear_screen()
        lokasi_rapi = " ".join(word.capitalize() for word in sub_menu.split())
        header = Panel(
            Text("HACKER NETWORK SIMULATION", justify="center", style="white"),
            border_style="green",
            title=f"{menu.upper()} - {sub_menu.upper()}",
            title_align="center",
        )
        info_text = Text()
        info_text.append(
            f"Menu Saat ini : {lokasi_rapi}\n", style="bold green"
        )
        info_text.append("Aktivitas     : ", style="bold green")
        peeked = self._log_aktivitas.peek()
        if peeked is not None:
            info_text.append_text(peeked)
        info = Group(
            info_text,
            "\n",
            f"Operator      : {self._operator}\n"
            f"Access        : {self._access_server}\n"
            f"Server        : {self._choosen_server}",
        )
        self._layout = Group(header, "\n", info, "\n")
        self._console.print(
            self._layout,
            Rule(style="white", characters="="),
            style="bold green",
        )

    # ── Main Menu ────────────────────────────────────────────────────────────

    def main_menu(self) -> None:
        """Menampilkan menu utama dan menangani navigasi tingkat atas."""
        self._log_aktivitas.add_log("Masuk ke Beranda")
        self._clear_screen()
        self._header_menu("Main Menu", "Beranda")
        try:
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
        except KeyboardInterrupt:
            return
        if choice == 0:
            with self._console.status("[bold red]Exiting..."):
                time.sleep(0.5)
                self._clear_screen()
                return
        self._sub_menu(choice)

    def _sub_menu(self, menu_id: int) -> None:
        """Mengarahkan ke sub-menu yang sesuai berdasarkan ID menu.

        Args:
            menu_id: ID menu tujuan.
                1 = Kelola Server
                2 = Network & Route
                3 = Traffic Queue
                4 = Struktur Data
                0 = Keluar

        """
        self._clear_screen()
        match menu_id:
            case 1:
                self._kelola_server_menu()
            case 2:
                self._network_route_menu()
            case 3:
                self._traffic_queue_menu()
            case 4:
                self._struktur_data_menu()

    # ── [1] Kelola Server ────────────────────────────────────────────────────

    def _kelola_server_menu(self) -> None:
        """Menampilkan sub-menu Kelola Server."""
        self._log_aktivitas.add_log("Masuk ke Kelola Server")
        self._clear_screen()
        self._header_menu("MENU", "Kelola Server")
        try:
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
        except KeyboardInterrupt:
            self.main_menu()
            return
        match choice:
            case 1:
                self._pilih_tampilkan_server()
            case 2:
                self._cari_server_berdasarkan_ip_server()
            case 3:
                self._urutkan_server_berdasarkan_bandwidth_server()
            case 4:
                self._monitoring_server_circular_server()
            case 0:
                self.main_menu()

    # ── [1.1] Pilih / Tampilkan Server ───────────────────────────────────────

    def _pilih_tampilkan_server(self) -> None:
        """Menampilkan dan memilih server dari daftar yang tersedia."""
        self._log_aktivitas.add_log(
            "Masuk ke Tampilkan dan Pilih Server", value=2
        )
        self._clear_screen()
        self._header_menu("SUB MENU", "Pilih / Tampilkan Server")
        self._server_carousel.run()
        self._node_from_server = (
            self._server_carousel.get_selected_server_node()
        )
        try:
            if self._node_from_server is not None:
                self._server_id = self._node_from_server.id
                self._server_carousel.make_footer()
                choice = make_menu_selection_question(
                    question=[
                        "Bruteforce Server Terpilih (server terpilih)",
                        "Kembali",
                    ],
                    value=[1, 0],
                ).ask()
            else:
                self._server_carousel.make_footer()
                choice = make_menu_selection_question(
                    question=["Kembali"],
                    value=[0],
                ).ask()
        except KeyboardInterrupt:
            self._kelola_server_menu()
            return
        match choice:
            case 1:
                self._bruteforce_selected_server()
            case 0:
                self._kelola_server_menu()

    def _bruteforce_selected_server(self) -> None:
        """Melakukan bruteforce login pada server yang dipilih.

        Hanya berjalan jika akses server belum UNLOCKED.
        """
        self._log_aktivitas.add_log(
            "Melakukan Bruteforce Server Terpilih", value=2
        )
        self._clear_screen()
        self._header_menu("SUB MENU", "Bruteforce Server Login")
        if self._access_server == "UNLOCKED":
            self._console.print(
                "[bold yellow]Akses UNLOCKED, bruteforce tidak perlu[/bold yellow]",
            )
            time.sleep(1)
            self._kelola_server_menu()
            return

        # Loading gimmick — simulasi bruteforce
        loading_stages = [
            "[bold yellow]Menyusun daftar kredensial...[/bold yellow]",
            "[bold yellow]Mencoba kombinasi username:password...[/bold yellow]",
            "[bold yellow]Menerobos firewall...[/bold yellow]",
            "[bold green]Akses berhasil![/bold green]",
        ]
        with self._console.status("") as status:
            for stage in loading_stages:
                status.update(stage)
                time.sleep(0.6)

        # Jalankan bruteforce
        result = bruteforce_server(self._server_id)

        if result is None:
            self._console.print(
                "\n[bold red]Bruteforce gagal — tidak ada kecocokan "
                "kredensial.[/bold red]",
            )
            try:
                self._console.input(
                    "[dim]\nTekan Enter untuk kembali...[/dim]",
                )
            except KeyboardInterrupt:
                pass
            self._kelola_server_menu()
            return

        # Update status akses server di data temporer
        for server in self._server_data["servers"]:
            if server["server_id"] == self._server_id:
                server["access"] = "UNLOCKED"
                break

        # Tampilkan hasil login dengan Rich Table
        table = Table(
            border_style="green",
            show_header=False,
            title_justify="center",
            expand=True,
        )
        table.add_column("Field", style="bold green", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_row("Server ID", result["server_id"])
        table.add_row("Server Name", result["server_name"])
        table.add_row("Final Access", result["access"])
        table.add_row("Username", result["username"])
        table.add_row("Password", result["password"])

        self._console.print()
        self._console.print(table)
        self._console.print()
        self._log_aktivitas.add_log(
            f"Bruteforce berhasil — {result['server_id']} "
            f"({result['server_name']})",
            value=2,
        )
        try:
            self._console.input(
                "[dim]\nTekan Enter untuk kembali ke menu server...[/dim]",
            )
        except KeyboardInterrupt:
            pass
        self._kelola_server_menu()

    # ── [1.2] Cari Server Berdasarkan IP ─────────────────────────────────────

    def _cari_server_berdasarkan_ip_server(self) -> None:
        """Menampilkan menu pencarian server berdasarkan alamat IP."""
        self._log_aktivitas.add_log("Masuk ke Cari Server Berdasarkan IP")
        self._clear_screen()
        self._header_menu("SUB MENU", "Cari Server Berdasarkan IP")
        try:
            choice = make_menu_selection_question(
                question=[
                    "Cari Menggunakan Binary Search",
                    "Cari Menggunakan Linear Search",
                    "Batalkan",
                ],
                value=[1, 2, 0],
            ).ask()
        except KeyboardInterrupt:
            self._kelola_server_menu()
            return
        match choice:
            case 1:
                self._cari_server_binary()
            case 2:
                self._cari_server_linear()
            case 0:
                self._kelola_server_menu()

    # ── [1.2.1] Binary Search ────────────────────────────────────────────────

    def _cari_server_binary(self) -> None:
        """Mencari server menggunakan binary search berdasarkan alamat IP."""
        self._log_aktivitas.add_log("Mencari IP Secara Binary", value=2)
        self._clear_screen()
        self._header_menu("SUB MENU", "Cari Server Berdasarkan IP")
        try:
            input_ip = ask_for_ip()
        except KeyboardInterrupt:
            self._cari_server_berdasarkan_ip_server()
            return
        if not input_ip:
            try:
                self._console.input(
                    "[dim]Tidak valid, masukkan ulang...[/dim]"
                )
            except KeyboardInterrupt:
                pass
            self._cari_server_berdasarkan_ip_server()
            return
        hasil_binary = cari_server_binary(input_ip)
        if not hasil_binary:
            try:
                self._console.input(
                    "[dim]Tidak valid, masukkan ulang...[/dim]"
                )
            except KeyboardInterrupt:
                pass
            self._cari_server_berdasarkan_ip_server()
        elif hasil_binary:
            panel_binary = display_search_ip_result(result=hasil_binary)
            self._console.print(panel_binary)
            try:
                self._console.input(
                    "[dim]\nTekan Enter untuk kembali ke menu...[/dim]"
                )
            except KeyboardInterrupt:
                pass
            self._cari_server_berdasarkan_ip_server()

    # ── [1.2.2] Linear Search ────────────────────────────────────────────────

    def _cari_server_linear(self) -> None:
        """Mencari server menggunakan linear search berdasarkan alamat IP."""
        self._log_aktivitas.add_log("Mencari IP Secara Linear", value=2)
        self._clear_screen()
        self._header_menu("SUB MENU", "Cari Server Berdasarkan IP")
        try:
            input_ip = ask_for_ip()
        except KeyboardInterrupt:
            self._cari_server_berdasarkan_ip_server()
            return
        try:
            hasil_linear = cari_server_linear(IPv4Address(input_ip))
        except AddressValueError:
            hasil_linear = False
        if not hasil_linear:
            try:
                self._console.input(
                    "[dim]Tidak valid, masukkan ulang...[/dim]"
                )
            except KeyboardInterrupt:
                pass
            self._cari_server_berdasarkan_ip_server()
        elif hasil_linear:
            panel_linier = display_search_ip_result(result=hasil_linear)
            self._console.print(panel_linier)
            try:
                self._console.input(
                    "[dim]\nTekan Enter untuk kembali ke menu...[/dim]"
                )
            except KeyboardInterrupt:
                pass
            self._cari_server_berdasarkan_ip_server()

    # ── [1.3] Urutkan Server Berdasarkan Bandwidth ───────────────────────────

    def _urutkan_server_berdasarkan_bandwidth_server(self) -> None:
        """Mengurutkan server berdasarkan bandwidth."""
        self._log_aktivitas.add_log(
            "Mengurutkan Server Berdasarkan Bandwidth", value=2
        )
        self._clear_screen()
        self._header_menu("SUB MENU", "Urutkan Server Berdasarkan Bandwidth")
        bandwidth_server: list[tuple[int, str, str, int]] = []
        for idx, req in enumerate(self._server_data["servers"]):
            bandwidth_server.append(
                (
                    idx,
                    req["server_id"],
                    req["server_name"],
                    req["bandwidth_mbps"],
                ),
            )
        self._console.print(
            tampilkan_bandwidth_progress(data=bandwidth_server)
        )
        try:
            choice = Confirm.ask(
                "Jalankan pengurutan?",
                console=self._console,
                default=True,
            )
        except KeyboardInterrupt:
            self._kelola_server_menu()
            return
        if choice:
            sorted_server = SortingServer().urutkan_server()
            with self._console.status(
                "[bold yellow]Mengurutkan server..."
            ) as status:
                time.sleep(1)
                status.update("[bold green]Server terurut...")
                time.sleep(1)
            self._console.print(
                tampilkan_bandwidth_progress(data=sorted_server, rank=True),
            )
            try:
                self._console.input(
                    "[dim]\nTekan Enter untuk kembali ke menu...[/dim]"
                )
            except KeyboardInterrupt:
                pass
            self._kelola_server_menu()
        else:
            self._kelola_server_menu()

    def _monitoring_server_circular_server(self) -> None:
        """Menampilkan monitoring server secara circular."""
        self._log_aktivitas.add_log(
            "Masuk ke Monitoring Server Circular", value=2
        )
        self._clear_screen()
        self._header_menu("SUB MENU", "Monitoring Server Circular")
        self._circular_server._make_circular_live_table()
        self._kelola_server_menu()

    # ── [1.4] Monitoring Server Circular ─────────────────────────────────────

    # ── [2] Network & Route ──────────────────────────────────────────────────

    def _network_route_menu(self) -> None:
        """Menampilkan sub-menu Network & Route."""
        self._log_aktivitas.add_log("Masuk ke Network & Route")
        self._clear_screen()
        self._header_menu("MENU", "Network & Route")
        try:
            choice = make_menu_selection_question(
                question=[
                    "Tampilkan Topologi Jaringan",
                    "Cari Rute Tercepat",
                    "Kembali ke Beranda",
                ],
                value=[1, 2, 0],
            ).ask()
        except KeyboardInterrupt:
            self.main_menu()
            return
        match choice:
            case 1:
                self._tampilkan_topologi_jaringan()
            case 2:
                self._cari_rute_tercepat_jaringan()
            case 0:
                self.main_menu()

    # ── [2.1] Tampilkan Topologi Jaringan ────────────────────────────────────

    def _tampilkan_topologi_jaringan(self) -> None:
        """Menampilkan topologi jaringan."""
        self._log_aktivitas.add_log(
            "Masuk ke Tampilkan Topologi Jaringan", value=2
        )
        self._clear_screen()
        self._header_menu("SUB MENU", "Tampilkan Topologi Jaringan")

        # Bangun graph dari data topologi
        graph = Graph()
        graph.build_from_json(
            Path("data/dalam-json/topologi.json"),
        )
        adj_list = graph.get_adjacency_list()

        # Tampilkan dalam format tree
        output = ""
        for server_id, edges in adj_list.items():
            output += f"├── {server_id}\n"
            for edge in edges:
                arah = "⇄" if edge["two_way"] else "→"
                output += (
                    f"|   ├── {arah} {edge['to']} ({edge['to_name']}) "
                    f"[{edge['latency_ms']}ms, {edge['bandwidth_mbps']}Mbps]\n"
                )
            if not edges:
                output += "|   ├── (tidak ada koneksi)\n"

        self._console.print(Panel(output.strip(), border_style="green"))
        try:
            self._console.input(
                "[dim]\nTekan Enter untuk kembali ke menu...[/dim]",
            )
        except KeyboardInterrupt:
            pass
        self._network_route_menu()

    # ── [2.2] Cari Rute Tercepat ─────────────────────────────────────────────

    def _cari_rute_tercepat_jaringan(self) -> None:
        """Mencari rute tercepat dalam jaringan."""
        self._log_aktivitas.add_log("Masuk ke Cari Rute Tercepat", value=2)
        self._clear_screen()
        self._header_menu("SUB MENU", "Cari Rute Tercepat")

        # Bangun graph
        graph = Graph()
        graph.build_from_json(
            Path("data/dalam-json/topologi.json"),
        )

        # Input server asal & tujuan pake FuzzyWordCompleter
        try:
            start = ask_for_server("Server asal: ")
        except KeyboardInterrupt:
            self._network_route_menu()
            return
        if start is None:
            self._network_route_menu()
            return

        try:
            end = ask_for_server("Server tujuan: ")
        except KeyboardInterrupt:
            self._network_route_menu()
            return
        if end is None:
            self._network_route_menu()
            return

        # Cari rute
        with self._console.status("[bold yellow]Mencari rute tercepat..."):
            time.sleep(0.8)
            result = graph.dijkstra(start, end)

        if result is None:
            self._console.print(
                "\n[bold red]Tidak ada jalur yang tersedia antara "
                f"{start} dan {end}.[/bold red]",
            )
            try:
                self._console.input(
                    "[dim]\nTekan Enter untuk kembali...[/dim]",
                )
            except KeyboardInterrupt:
                pass
            self._network_route_menu()
            return

        # Tampilkan hasil
        table = Table(
            border_style="green", title_justify="center", expand=True
        )
        table.add_column("Info", style="bold green", no_wrap=True)
        table.add_column("Detail", style="white")
        table.add_row("Dari", f"{result['from']} ({result['from_name']})")
        table.add_row("Tujuan", f"{result['to']} ({result['to_name']})")
        table.add_row(
            "Total Latency",
            f"{result['total_latency_ms']} ms",
        )
        table.add_row(
            "Min Bandwidth",
            f"{result['min_bandwidth_mbps']} Mbps",
        )

        # Tabel hop
        hop_table = Table(
            border_style="green",
            show_header=True,
            title_justify="center",
            expand=True,
        )
        hop_table.add_column("Hop", style="bold green")
        hop_table.add_column("Dari", style="white")
        hop_table.add_column("Ke", style="white")
        hop_table.add_column("Latency", style="white")
        hop_table.add_column("Bandwidth", style="white")

        for i, hop in enumerate(result["path"], start=1):
            arah = "⇄" if hop["two_way"] else "→"
            hop_table.add_row(
                str(i),
                f"{hop['from']} ({hop['from_name']})",
                f"{arah} {hop['to']} ({hop['to_name']})",
                f"{hop['latency_ms']} ms",
                f"{hop['bandwidth_mbps']} Mbps",
            )

        self._console.print()
        self._console.print(table)
        self._console.print()
        self._console.print(hop_table)
        self._console.print()
        self._log_aktivitas.add_log(
            f"Rute tercepat {start} → {end}: {result['total_latency_ms']}ms",
            value=2,
        )
        try:
            self._console.input(
                "[dim]\nTekan Enter untuk kembali ke menu...[/dim]",
            )
        except KeyboardInterrupt:
            pass
        self._network_route_menu()

    # ── [3] Traffic Queue ────────────────────────────────────────────────────

    def _traffic_queue_menu(self) -> None:
        """Menampilkan sub-menu Traffic Queue."""
        self._log_aktivitas.add_log("Masuk ke Traffic Queue")
        self._clear_screen()
        self._header_menu("MENU", "Traffic Queue")
        self._console.print(
            f"Queue Size: {self._traffic.size()}",
            end="\n\n",
            style="bold yellow",
        )
        try:
            choice = make_menu_selection_question(
                question=[
                    "Tampilkan Queue Traffic",
                    "Kelola Traffic",
                    "Kembali ke Beranda",
                ],
                value=[1, 2, 0],
            ).ask()
        except KeyboardInterrupt:
            self.main_menu()
            return
        match choice:
            case 1:
                self._tampilkan_queue_traffic()
            case 2:
                self._kelola_traffic()
            case 0:
                self.main_menu()

    # ── [3.1] Tampilkan Queue Traffic ────────────────────────────────────────

    def _tampilkan_queue_traffic(self) -> None:
        """Menampilkan seluruh antrian traffic."""
        self._log_aktivitas.add_log("Masuk ke Tampilkan Queue Traffic")
        self._log_aktivitas.add_log("Menampilkan Queue Traffic", value=2)
        self._header_menu("SUB MENU", "Tampilkan Queue Traffic")
        self._traffic.display()
        try:
            choice = make_menu_selection_question(
                question=["Kembali ke Traffic Queue"],
                value=[0],
            ).ask()
        except KeyboardInterrupt:
            self._traffic_queue_menu()
            return
        match choice:
            case 0:
                self._traffic_queue_menu()

    # ── [3.2] Kelola Traffic ─────────────────────────────────────────────────

    def _kelola_traffic(self) -> None:
        """Menampilkan menu pengelolaan traffic."""
        self._log_aktivitas.add_log("Masuk ke Kelola Traffic")
        self._clear_screen()
        self._header_menu("SUB MENU", "Kelola Traffic")
        try:
            choice = make_menu_selection_question(
                question=[
                    "Lihat Traffic Terdepan",
                    "Proses Traffic Terdepan",
                    "Kembali ke Traffic Queue",
                ],
                value=[1, 2, 0],
            ).ask()
        except KeyboardInterrupt:
            self._traffic_queue_menu()
            return
        match choice:
            case 1:
                self._lihat_traffic_terdepan_traffic()
            case 2:
                self._proses_traffic_terdepan_traffic()
            case 0:
                self._traffic_queue_menu()

    # ── [3.2.1] Lihat Traffic Terdepan ───────────────────────────────────────

    def _lihat_traffic_terdepan_traffic(self) -> None:
        """Menampilkan traffic terdepan dalam antrian."""
        self._log_aktivitas.add_log("Masuk ke Lihat Traffic Terdepan")
        self._log_aktivitas.add_log("Melihat Traffic Terdepan", value=2)
        self._header_menu("SUB MENU", "Lihat Traffic Terdepan")
        self._traffic.display_front()
        try:
            choice = make_menu_selection_question(
                question=["Kembali ke Kelola Traffic"],
                value=[0],
            ).ask()
        except KeyboardInterrupt:
            self._kelola_traffic()
            return
        match choice:
            case 0:
                self._kelola_traffic()

    # ── [3.2.2] Proses Traffic Terdepan ──────────────────────────────────────

    def _proses_traffic_terdepan_traffic(self) -> None:
        """Memproses traffic terdepan dalam antrian."""
        self._log_aktivitas.add_log("Masuk ke Proses Traffic Terdepan")
        self._log_aktivitas.add_log("Memproses Traffic Terdepan", value=2)
        self._header_menu("SUB MENU", "Proses Traffic Terdepan")
        self._traffic.display_dequeue()
        try:
            choice = make_menu_selection_question(
                question=["Kembali ke Kelola Traffic"],
                value=[0],
            ).ask()
        except KeyboardInterrupt:
            self._kelola_traffic()
            return
        match choice:
            case 0:
                self._kelola_traffic()

    # ── [4] Struktur Data ────────────────────────────────────────────────────

    def _struktur_data_menu(self) -> None:
        """Menampilkan sub-menu Struktur Data."""
        self._log_aktivitas.add_log("Masuk ke Struktur Data")
        self._clear_screen()
        self._header_menu("MENU", "Struktur Data")
        try:
            choice = make_menu_selection_question(
                question=[
                    "Tampilkan Folder Server",
                    "Kelola Stack Log Aktivitas",
                    "Kembali ke Beranda",
                ],
                value=[1, 2, 0],
            ).ask()
        except KeyboardInterrupt:
            self.main_menu()
            return
        match choice:
            case 1:
                self._tampilkan_folder_server_data()
            case 2:
                self._kelola_stack_log_aktivitas_data()
            case 0:
                self.main_menu()

    # ── [4.1] Tampilkan Folder Server ────────────────────────────────────────

    def _tampilkan_folder_server_data(self) -> None:
        """Menampilkan folder server dengan traversal tree."""
        self._log_aktivitas.add_log(
            "Masuk ke Tampilkan Folder Server", value=2
        )
        self._clear_screen()
        self._header_menu("SUB MENU", "Tampilkan Folder Server")
        server_tree = ServerTreeBuilder.build_server_tree()
        try:
            choice = make_menu_selection_question(
                question=["Preorder", "Inorder", "Postorder", "Batalkan"],
                value=[1, 2, 3, 0],
            ).ask()
        except KeyboardInterrupt:
            self._struktur_data_menu()
            return
        pilihan_traversal = None
        if choice == TRAVERSAL_PREORDER:
            pilihan_traversal = "preorder"
        elif choice == TRAVERSAL_INORDER:
            pilihan_traversal = "inorder"
        elif choice == TRAVERSAL_POSTORDER:
            pilihan_traversal = "postorder"
        else:
            self._struktur_data_menu()
            return
        server_tree = ServerTreeBuilder.build_server_tree()
        target_id = self._server_id
        for item in server_tree:
            match = re.search(r"\((SRV\d+)\)", item.name)
            if match:
                server_id = match.group(1)
                if server_id == target_id:
                    pr, inor, post = (
                        preorder(item),
                        inorder(item),
                        postorder(item),
                    )
                    if pilihan_traversal is not None:
                        p, t = make_traversal_folder(
                            pilihan_traversal=pilihan_traversal,
                            preorder=pr,
                            inorder=inor,
                            postorder=post,
                        )
                        self._console.print(p, t)
                    break
        else:
            self._console.print("[bold red]Tidak ditemukan")
        try:
            self._console.input(
                "[dim]\nTekan Enter untuk kembali ke menu...[/dim]"
            )
        except KeyboardInterrupt:
            pass
        self._struktur_data_menu()

    # ── [4.2] Kelola Stack Log Aktivitas ─────────────────────────────────────

    def _kelola_stack_log_aktivitas_data(self) -> None:
        """Mengelola stack log aktivitas."""
        self._log_aktivitas.add_log("Masuk ke Kelola Stack Log Aktivitas")
        self._clear_screen()
        self._header_menu("SUB MENU", "Kelola Stack Log Aktivitas")
        self._log_aktivitas.show_logs()
        try:
            choice = make_menu_selection_question(
                question=[
                    "Hapus log teratas",
                    "Hapus seluruh log",
                    "Kembali ke Struktur Data",
                ],
                value=[1, 2, 0],
            ).ask()
        except KeyboardInterrupt:
            self._struktur_data_menu()
            return
        self._clear_screen()
        match choice:
            case 1:
                self._header_menu("SUB MENU", "Kelola Stack Log Aktivitas")
                self._log_aktivitas.pop()
                self._log_aktivitas.show_logs()
                self._console.print(
                    "\n[bold yellow]Log teratas berhasil dihapus. "
                    "Kembali ke menu Struktur Data...[/bold yellow]",
                )
                time.sleep(2)
                self._struktur_data_menu()
            case 2:
                self._header_menu("SUB MENU", "Kelola Stack Log Aktivitas")
                self._log_aktivitas.clear_log()
                self._log_aktivitas.show_logs()
                self._console.print(
                    "\n[bold yellow]Seluruh log berhasil dihapus. "
                    "Kembali ke menu Struktur Data...[/bold yellow]",
                )
                time.sleep(2)
                self._struktur_data_menu()
            case 0 | None:
                self._struktur_data_menu()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.intro()
    main_menu.main_menu()
