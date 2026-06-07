"""@author: Abdullah Affandi."""

# FULL PROMPT TOOLKIT jangan digabungkan dengan RICH
from prompt_toolkit import print_formatted_text
from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import FormattedTextControl, Layout, Window
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from src import FungsiServer, ServerNode


class ServerCarouselNode:
    """Node untuk doubly linked list carousel server.

    Attributes:
        data: Data server yang disimpan dalam node.
        prev: Pointer ke node sebelumnya dalam doubly linked list.
        next: Pointer ke node berikutnya dalam doubly linked list.
    """

    # Ini jangan diimport ya
    def __init__(self, data: ServerNode) -> None:
        """Inisialisasi node dengan data server.

        Args:
            data: Objek ServerNode yang akan disimpan dalam node.
        """
        self.data = data
        self.prev: ServerCarouselNode | None = None
        self.next: ServerCarouselNode | None = None


# Global function
# run - menjalankan aplikasi
# get_selected_server_node - mendapatkan node server terpilih
# make_footer - langsung nampilkan footer
class ServerCarousel(FungsiServer):
    """Carousel server dengan navigasi doubly linked list.

    Menyediakan navigasi server menggunakan struktur data doubly linked list
    dengan antarmuka prompt_toolkit untuk navigasi keyboard.

    Attributes:
        current: Node yang sedang aktif dalam carousel.
        head: Node pertama dalam doubly linked list.
        selected: Node server yang terpilih.
        console: Console Rich untuk menampilkan output.
        bindings: Key bindings untuk navigasi keyboard.
        app: Aplikasi prompt_toolkit.
        layout: Layout tampilan saat ini.
        table: Tabel Rich untuk daftar server.
    """

    def __init__(self, selected_id: str | None = None) -> None:
        """Inisialisasi carousel dengan data server dari parent class.

        Args:
            selected_id: ID server yang akan dipilih saat inisialisasi.
        """
        super().__init__()
        super().tambah_server()

        # Akan digunakan untuk sebagai penampung ServerCarouselNode
        self.current: ServerCarouselNode | None = None
        self._initialize_node()

        self.selected: ServerNode | None = None
        if selected_id:
            self._restore_state(selected_id)
        elif self.current is not None:
            # str self.current.data.id
            self._restore_state(self.current.data.id)

        self.console = Console()
        self.bindings = KeyBindings()
        self._register_bind_keys()
        self.current_copy: ServerCarouselNode | None = None
        self.app: Application | None = None
        self.layout: Panel | None = None
        self.table: Table | None = None

    def run(self) -> Application:
        """Menjalankan aplikasi carousel server.

        Returns:
            Objek Application prompt_toolkit yang telah dijalankan.
        """
        self.app = self._make_app()

        self.app.run()

        return self.app

    def get_selected_server_node(self) -> ServerNode | None:
        """Mengembalikan node server yang terpilih.

        Returns:
            Objek ServerNode yang terpilih, atau None jika belum ada.
        """
        return self.selected

    def make_footer(self) -> None:
        """Menampilkan footer dengan prompt toolkit print_formatted_text."""
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
        """Inisialisasi seluruh node dari server_list."""
        self.head: ServerCarouselNode | None = (
            None  # Simpan referensi ke node pertama
        )

        for server in self.server_list:
            new_node = ServerCarouselNode(server)

            if self.current is None:
                self.current = new_node
                self.head = new_node  # catat head
            else:
                self.current.next = new_node
                new_node.prev = self.current

            self.current = new_node

        self.current = self.head

    def _restore_state(self, selected_id: str) -> None:
        """Memuat ulang state ke server yang dipilih sebelumnya.

        Args:
            selected_id: ID server yang akan dipulihkan.
        """
        node: ServerCarouselNode | None = self.head  # mulai dari head
        while node is not None:
            if str(node.data.id) == str(selected_id):
                self.current = node  # pindahkan current ke node yang cocok
                return
            node = node.next

    def _selected_server(self) -> ServerNode | None:
        """Inisialisasi node current dengan server terpilih (internal).

        Returns:
            Objek ServerNode yang terpilih.
        """
        if self.current is not None:
            self.selected = self.current.data
        return self.selected

    def _add_server_row(
        self, position: str, server: ServerNode | None, selected: bool = False
    ) -> None:
        """Membuat baris tabel untuk posisi PREVIOUS/SELECTED/NEXT.

        Args:
            position: Label posisi (PREVIOUS, SELECTED, NEXT).
            server: Data server yang akan ditampilkan.
            selected: Apakah baris ini adalah server yang terpilih.
        """
        if server is None:
            self.table.add_row(position, "-", "-", "-", "-", style="dim")
            return

        status: str = str(server.status).strip().upper()

        status_style: str = {
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
        """Membuat kolom tabel untuk daftar server.

        Returns:
            Objek Table Rich dengan kolom yang telah ditentukan.
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
        """Membuat tabel daftar server (PREVIOUS, SELECTED, NEXT).

        Returns:
            Panel Rich berisi tabel daftar server.
        """
        self.table = self._make_table()  # refresh table setiap kali

        prev_data: ServerNode | None = (
            self.current.prev.data
            if self.current and self.current.prev
            else None
        )
        next_data: ServerNode | None = (
            self.current.next.data
            if self.current and self.current.next
            else None
        )

        self._add_server_row("PREVIOUS", prev_data)
        if self.current is not None:
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
        """Pindah ke node berikutnya."""
        if self.current is not None and self.current.next is not None:
            self.current = self.current.next

    def _go_prev(self) -> None:
        """Pindah ke node sebelumnya."""
        if self.current is not None and self.current.prev is not None:
            self.current = self.current.prev

    def _make_server_detail(self) -> Panel:
        """Membuat panel detail server yang sedang dipilih.

        Returns:
            Panel Rich berisi detail server.
        """
        if self.current is None:
            return Panel(
                Text("Tidak ada server yang dipilih.", style="bold red"),
                title="[bold]DETAIL SERVER[/bold]",
                border_style="red",
                padding=(1, 4),
                width=self.console.width - 2,
            )

        server: ServerNode = self.current.data
        status: str = str(server.status).strip().upper()

        status_style: str = {
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

        sid: str = f"[bold cyan]{server.id}[/bold cyan]"
        sname: str = f"[bold white]{server.nama}[/bold white]"
        sip: str = f"[bold yellow]{server.ip}[/bold yellow]"
        sstat: str = f"[{status_style}]{status}[/{status_style}]"

        table.add_row("[bold]Server ID[/bold]", ":", sid)
        table.add_row("[bold]Server Name[/bold]", ":", sname)
        table.add_row("[bold]IP Address[/bold]", ":", sip)
        table.add_row("[bold]Status[/bold]", ":", sstat)

        return Panel(
            table,
            title="[bold]DETAIL SERVER YANG DIPILIH[/bold]",
            border_style="green",
            padding=(1, 4),
            width=self.console.width - 2,
        )

    def _get_current_table(self) -> ANSI:
        """Menangkap tampilan tabel terbaru sebagai ANSI.

        Returns:
            Objek ANSI dari prompt_toolkit berisi tampilan tabel.
        """
        self.console.begin_capture()

        deskripsi = Text.from_markup(
            "[bold cyan]Navigasi:[/bold cyan] "
            "[reverse] \u2191 [/reverse] Atas  "
            "[reverse] \u2193 [/reverse] Bawah  "
            "[reverse] Enter [/reverse] Pilih Server  "
            "[reverse] Q [/reverse] Keluar"
        )

        self.console.print(deskripsi)
        self.console.print(self._make_server_list_table())
        self.console.print(self._make_server_detail())
        return ANSI(self.console.end_capture())

    def _make_app(self) -> Application:
        """Membuat aplikasi prompt toolkit.

        Returns:
            Objek Application prompt_toolkit yang siap dijalankan.
        """
        app = Application(
            layout=Layout(
                Window(
                    FormattedTextControl(text=self._get_current_table),
                    always_hide_cursor=True,
                )
            ),
            key_bindings=self.bindings,
        )

        return app

    def _register_bind_keys(self) -> None:
        """Melakukan registrasi key bindings untuk navigasi keyboard."""

        @self.bindings.add("down")
        def _go_next_handler(_event) -> None:
            self._go_next()

        @self.bindings.add("up")
        def _go_prev_handler(_event) -> None:
            self._go_prev()

        @self.bindings.add("q")
        @self.bindings.add("escape")
        @self.bindings.add("c-c")
        def _exit_handler(_event) -> None:
            if self.selected is not None:
                self._restore_state(self.selected.id)
                self.app.invalidate()
                self.app.loop.call_later(0.1, self.app.exit)
            else:
                self.app.exit()

        @self.bindings.add("enter")
        def _select_handler(_event) -> None:
            self._selected_server()
            self.app.exit()


if __name__ == "__main__":
    carousel = ServerCarousel()
    carousel.run()
    carousel.make_footer()
