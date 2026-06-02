"""
@author: Abdullah Affandi
"""

# FULL PROMPT TOOLKIT jangan digabungkan dengan RICH
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import Application
from prompt_toolkit.layout import FormattedTextControl, Layout, Window
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit import print_formatted_text

from rich.text import Text
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src import FungsiServer


class ServerCarouselNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class ServerCarousel(FungsiServer):
    def __init__(self):
        # return self.server_list
        # self.id = id
        # self.nama = nama
        # self.ip = ip
        # self.status = status
        super().__init__()
        super().tambah_server()

        # Akan digunakan untuk sebagai penampun ServerCarouselNode
        self.current = None
        self._initialize_node()

        self.console = Console()
        self.bindings = KeyBindings()
        self._register_bind_keys()

    def _initialize_node(self):
        head = None  # Simpan referensi ke node pertama

        for server in self.server_list:
            new_node = ServerCarouselNode(server)

            if self.current is None:
                self.current = new_node
                head = new_node  # catat head
            else:
                self.current.next = new_node
                new_node.prev = self.current

            self.current = new_node

        self.current = head

    def _add_server_row(self, position: str, server, selected: bool = False) -> None:
        if server is None:
            self.table.add_row(position, "-", "-", "-", "-", style="dim")
            return

        status = str(server.status).strip().upper()

        status_style = {
            "ONLINE": "bold green",
            "OFFLINE": "bold red",
            "MAINTENANCE": "bold yellow",
            "BLOCKED": "bold red",
            "OVERLOAD": "bold magenta",
        }.get(status, "white")

        if selected:
            self.table.add_row(
                "[bold green]SELECTED[/bold green]",
                f"[bold cyan]{server.id}[/bold cyan]",
                f"[bold white]{server.nama}[/bold white]",
                f"[bold yellow]{server.ip}[/bold yellow]",
                f"[{status_style}]{status}[/{status_style}]",
            )
            return

        self.table.add_row(
            position,
            str(server.id),
            str(server.nama),
            str(server.ip),
            f"[{status_style}]{status}[/{status_style}]",
        )

    def _make_table(self) -> Table:
        table = Table(
            box=None,
            expand=True,
            show_header=True,
            show_edge=False,
            pad_edge=False,
            header_style="green_yellow",
        )

        table.add_column("Position", justify="left", ratio=1)
        table.add_column("Server ID", justify="left", ratio=1)
        table.add_column("Server Name", justify="left", ratio=1)
        table.add_column("IP Address", justify="left", ratio=1)
        table.add_column("Status", justify="left", ratio=1)

        return table

    def _make_server_list_table(self) -> Panel:
        self.table = self._make_table()  # refresh table setiap kali

        prev_data = self.current.prev.data if self.current.prev else None
        next_data = self.current.next.data if self.current.next else None

        self._add_server_row("PREVIOUS", prev_data)
        self._add_server_row("SELECTED", self.current.data, selected=True)
        self._add_server_row("NEXT", next_data)

        return Panel(
            self.table,
            title="DAFTAR SERVER",
            border_style="green",
            padding=(1, 4),
            width=self.console.width - 2
        )

    def _go_next(self):
        if self.current.next is not None:
            self.current = self.current.next

    def _go_prev(self):
        if self.current.prev is not None:
            self.current = self.current.prev

    def _get_current_table(self):
        # Fungsi pembantu untuk menangkap tabel terbaru
        self.console.begin_capture()

        deskripsi = Text.from_markup(
            "[bold cyan]Navigasi:[/bold cyan] "
            "[reverse] ↑ [/reverse] Atas  "
            "[reverse] ↓ [/reverse] Bawah  "
            "[reverse] Enter [/reverse] Pilih Server  "
            "[reverse] Q [/reverse] Keluar"
        )

        self.console.print(deskripsi)
        self.console.print(self._make_server_list_table())
        return ANSI(self.console.end_capture())

    def _make_app(self) -> Application:
        app = Application(
            layout=Layout(
                Window(
                    FormattedTextControl(text=lambda: self._get_current_table()),
                    always_hide_cursor=True,
                )
            ),
            key_bindings=self.bindings,
        )

        return app

    def run(self) -> Application:
        self.app = self._make_app()

        self.app.run()

        return self.app

    def _register_bind_keys(self):
        @self.bindings.add("down")
        def _(event):
            self._go_next()

        @self.bindings.add("up")
        def _(event):
            self._go_prev()

        @self.bindings.add("q")
        @self.bindings.add("escape")
        @self.bindings.add("c-c")
        def _(event):
            self.app.exit()

        @self.bindings.add("enter")
        def _(event):
            self.app.exit()
            


if __name__ == "__main__":
    carousel = ServerCarousel()
    carousel.run()
