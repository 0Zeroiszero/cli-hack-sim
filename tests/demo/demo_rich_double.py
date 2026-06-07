"""
Demo Double Linked List Carousel dengan Rich
@author: Abdullah Affandi
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from src.server import Server

console = Console()


class ServerNode(Server):
    def __init__(self, *, server_id: str, server_name: str, ip: str, status: str):
        super().__init__(
            nama=server_name,
            id=server_id,
            ip=ip,
            status=status,
        )

        self.prev = None
        self.next = None


class ServerCarousel:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_server(self, *, server_id: str, server_name: str, ip: str, status: str):
        new_node = ServerNode(
            server_id=server_id,
            server_name=server_name,
            ip=ip,
            status=status,
        )

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def move_up(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        else:
            console.print(
                "[bold yellow]Sudah berada di server paling atas.[/bold yellow]"
            )
            console.input("Tekan Enter untuk lanjut...")

    def move_down(self):
        if self.current and self.current.next:
            self.current = self.current.next
        else:
            console.print(
                "[bold yellow]Sudah berada di server paling bawah.[/bold yellow]"
            )
            console.input("Tekan Enter untuk lanjut...")

    def display_carousel(self) -> None:
        if self.current is None:
            console.print("[bold red]Data server kosong.[/bold red]")
            return

        table = Table(
            title="DAFTAR SERVER",
            box=box.SIMPLE_HEAVY,
            show_lines=False,
        )

        table.add_column("Position", justify="center", style="bold")
        table.add_column("Server ID", justify="center")
        table.add_column("Server Name")
        table.add_column("IP Address")
        table.add_column("Status", justify="center")

        if self.current.prev:
            table.add_row(
                "PREVIOUS",
                self.current.prev.id,
                self.current.prev.nama,
                self.current.prev.ip,
                self.current.prev.status,
                style="dim green",
            )

        table.add_row(
            "SELECTED",
            self.current.id,
            self.current.nama,
            self.current.ip,
            self.current.status,
            style="bold green",
        )

        if self.current.next:
            table.add_row(
                "NEXT",
                self.current.next.id,
                self.current.next.nama,
                self.current.next.ip,
                self.current.next.status,
                style="dim green",
            )

        console.print(table)

    def show_current_detail(self) -> None:
        if self.current is None:
            console.print("[bold red]Tidak ada server yang dipilih.[/bold red]")
            return

        detail = Table(show_header=False, box=None)
        detail.add_column("Field", style="bold white")
        detail.add_column("Value", style="bold green")

        detail.add_row("Server ID", self.current.id)
        detail.add_row("Server Name", self.current.nama)
        detail.add_row("IP Address", self.current.ip)
        detail.add_row("Status", self.current.status)

        console.print(
            Panel(
                detail,
                title="DETAIL SERVER YANG DIPILIH",
                border_style="green",
            )
        )

    def display_controls(self) -> None:
        controls = (
            "[bold cyan][W][/bold cyan] Naik ke server sebelumnya\n"
            "[bold cyan][S][/bold cyan] Turun ke server berikutnya\n"
            "[bold cyan][Q][/bold cyan] Keluar"
        )

        console.print(
            Panel(
                controls,
                title="KONTROL",
                border_style="cyan",
            )
        )

    def run(self):
        while True:
            console.clear()

            self.display_carousel()
            self.show_current_detail()
            self.display_controls()

            choice = console.input("\n[bold white]Pilih:[/bold white] ").lower().strip()

            if choice == "w":
                self.move_up()
            elif choice == "s":
                self.move_down()
            elif choice == "q":
                break
            else:
                console.print("[bold red]Pilihan tidak valid.[/bold red]")
                console.input("Tekan Enter untuk lanjut...")


if __name__ == "__main__":
    carousel = ServerCarousel()

    carousel.add_server(
        server_id="SRV001",
        server_name="Server Alpha",
        ip="192.168.1.10",
        status="ONLINE",
    )

    carousel.add_server(
        server_id="SRV002",
        server_name="Server Beta",
        ip="192.168.1.20",
        status="ONLINE",
    )

    carousel.add_server(
        server_id="SRV003",
        server_name="Server Gamma",
        ip="192.168.1.30",
        status="OFFLINE",
    )

    carousel.run()
