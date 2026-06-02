"""
@author: Abdullah Affandi
"""

# FULL PROMPT TOOLKIT jangan digabungkan dengan RICH
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import Application
from prompt_toolkit.layout import FormattedTextControl, Layout, Window
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit import print_formatted_text

from rich.rule import Rule
from rich.text import Text
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from src import FungsiServer, ServerNode
from DSA import LogAktivitas


class ServerCarouselNode:
    # Ini jangan diimport ya
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


# Global function
# run - menjalankan aplikasi
# get_selected_server_node - mendapatkan node server terpilih
# make_footer - langsung nampilkan footer
class ServerCarousel(FungsiServer):
    def __init__(self, selected_id: str = None):
        # return self.server_list
        # self.id = id
        # self.nama = nama
        # self.ip = ip
        # self.status = status

        # self.current merujuk kepada ServerCarouselNode
        # self.current.data merujuk pada ServerNode
        super().__init__()
        super().tambah_server()

        # Akan digunakan untuk sebagai penampung ServerCarouselNode
        self.current = None
        self._initialize_node()

        self.selected = None
        if selected_id:
            self._restore_state(selected_id)
        elif self.selected:
            # str self.current.data.id
            self._restore_state(self.current.data.id)

        self.console = Console()
        self.bindings = KeyBindings()
        self._register_bind_keys()

    def run(self) -> Application:
        """
        Menjalankan aplikasi
        """
        self.app = self._make_app()

        self.app.run()

        return self.app

    def get_selected_server_node(self) -> ServerNode:
        """
        Pemakaian luar atau dalam class
        """
        return self.selected

    def make_footer(self) -> None:
        """
        Langsung nampilkan footer dengan memanfaatkan prompt toolkit
        print_formatted_text
        """
        self.console.begin_capture()
        self.console.print(
            Rule(style="white", characters="="), width=self.console.width - 2
        )

        footer = Panel(
            Text("AKSI SERVER TERPILIH", justify="center", style="white"),
            border_style="white",
            title_align="center",
            width=self.console.width - 2,
        )

        self.layout = footer
        self.console.print(
            self.layout,
            Rule(style="white", characters="="),
            width=self.console.width - 2,
        )

        print_formatted_text(ANSI(self.console.end_capture()))

    def _initialize_node(self) -> None:
        """
        Inisialisasi seluruh Node
        """
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

    def _restore_state(self, selected_id: str) -> None:
        """
        Jika udah milih server, state-nya akan dimuat ulang (mirip save game)
        """
        node = self.current  # mulai dari head
        while node is not None:
            if node.data.id == selected_id:
                self.current = node  # pindahkan current ke node yang cocok
                return
            node = node.next

    def _selected_server(self) -> ServerNode:
        """
        Hanya untuk pemakaian dalam class
        Melakukan inisialiasi node current dengan server terpilih
        """
        self.selected = self.current.data

    def _add_server_row(self, position: str, server, selected: bool = False) -> None:
        """
        Helper untuk membuat baris tabel yang dipanggil _make_server_list_table
        """
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
        """
        Helper untuk membuat kolom tabel yang dipanggil _make_server_list_table
        """
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
        """
        Membuat list tabel PREVIOUS, SELECTED, NEXT untuk ditampilkan
        """
        self.table = self._make_table()  # refresh table setiap kali

        prev_data = self.current.prev.data if self.current.prev else None
        next_data = self.current.next.data if self.current.next else None

        self._add_server_row("PREVIOUS", prev_data)
        self._add_server_row("SELECTED", self.current.data, selected=True)
        self._add_server_row("NEXT", next_data)

        return Panel(
            self.table,
            title="DAFTAR SERVER",
            border_style="bold green",
            padding=(1, 4),
            width=self.console.width - 2,
        )

    def _go_next(self) -> None:
        """
        Next Node
        """
        if self.current.next is not None:
            self.current = self.current.next

    def _go_prev(self) -> None:
        """
        Previous Node
        """
        if self.current.prev is not None:
            self.current = self.current.prev

    def _make_server_detail(self) -> Panel:
        server = self.current.data
        status = str(server.status).strip().upper()

        status_style = {
            "ONLINE": "bold green",
            "OFFLINE": "bold red",
            "MAINTENANCE": "bold yellow",
            "BLOCKED": "bold red",
            "OVERLOAD": "bold magenta",
        }.get(status, "white")

        table = Table(
            box=None,
            expand=True,
            show_header=False,
            show_edge=False,
            pad_edge=False,
        )

        table.add_column("Key", justify="left", ratio=1)
        table.add_column("Sep", justify="center", ratio=0)
        table.add_column("Value", justify="left", ratio=2)

        table.add_row(
            "[bold]Server ID[/bold]", ":", f"[bold cyan]{server.id}[/bold cyan]"
        )
        table.add_row(
            "[bold]Server Name[/bold]", ":", f"[bold white]{server.nama}[/bold white]"
        )
        table.add_row(
            "[bold]IP Address[/bold]", ":", f"[bold yellow]{server.ip}[/bold yellow]"
        )
        table.add_row(
            "[bold]Status[/bold]", ":", f"[{status_style}]{status}[/{status_style}]"
        )

        return Panel(
            table,
            title="[bold]DETAIL SERVER YANG DIPILIH[/bold]",
            border_style="green",
            padding=(1, 4),
            width=self.console.width - 2,
        )

    def _get_current_table(self) -> None:
        """
        Fungsi pembantu untuk menangkap tabel terbaru
        """
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
        self.console.print(self._make_server_detail())
        return ANSI(self.console.end_capture())

    def _make_app(self) -> Application:
        """
        Membuat aplikasi prompt toolkit
        """
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

    def _register_bind_keys(self) -> None:
        """
        Melakukan registrasi bindings
        """

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
                if self.selected is not None:
                    self._restore_state(self.selected.id)
                    self.app.invalidate()
                    self.app.loop.call_later(0.1, self.app.exit)  # exit setelah render
                else:
                    self.app.exit()

        @self.bindings.add("enter")
        def _(event):
            self._selected_server()
            self.app.exit()


if __name__ == "__main__":
    carousel = ServerCarousel()
    carousel.run()
    carousel.make_footer()
