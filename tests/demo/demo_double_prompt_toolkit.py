"""
Table Carousel dengan Doubly Linked List
- Navigasi ← → untuk berpindah halaman (node)
- Navigasi ↑ ↓ untuk memilih baris dalam tabel
- Tabel dirender dengan Rich, key binding dengan prompt_toolkit
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.formatted_text import ANSI


# ─────────────────────────────────────────────
#  DOUBLY LINKED LIST
# ─────────────────────────────────────────────


@dataclass
class TableNode:
    """Satu node = satu halaman tabel."""

    title: str
    columns: List[str]
    rows: List[List[Any]]
    prev: Optional["TableNode"] = field(default=None, repr=False)
    next: Optional["TableNode"] = field(default=None, repr=False)


class TableCarousel:
    """Doubly linked list yang menyimpan node-node tabel."""

    def __init__(self):
        self.head: Optional[TableNode] = None
        self.tail: Optional[TableNode] = None
        self.current: Optional[TableNode] = None
        self._size: int = 0

    def append(self, title: str, columns: List[str], rows: List[List[Any]]) -> None:
        node = TableNode(title=title, columns=columns, rows=rows)
        if self.tail is None:
            self.head = self.tail = node
            self.current = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    def go_next(self) -> bool:
        """Pindah ke node berikutnya. Return True jika berhasil."""
        if self.current and self.current.next:
            self.current = self.current.next
            return True
        return False

    def go_prev(self) -> bool:
        """Pindah ke node sebelumnya. Return True jika berhasil."""
        if self.current and self.current.prev:
            self.current = self.current.prev
            return True
        return False

    @property
    def size(self) -> int:
        return self._size

    def position(self) -> int:
        """Indeks posisi current node (1-based)."""
        node = self.head
        idx = 1
        while node and node is not self.current:
            node = node.next
            idx += 1
        return idx


# ─────────────────────────────────────────────
#  RENDER TABEL DENGAN RICH
# ─────────────────────────────────────────────

console = Console()


def render_table(
    node: TableNode,
    selected_row: int,
    position: int,
    total: int,
    width: int = 80,
) -> str:
    """Render node tabel ke string ANSI menggunakan Rich."""

    import io
    from rich.console import Console as _Console

    buf = io.StringIO()
    c = _Console(file=buf, force_terminal=True, width=width, highlight=False)

    # ── Header / Judul ──────────────────────────────────────────────
    nav_hint = Text()
    if position > 1:
        nav_hint.append("← Prev  ", style="bold cyan")
    else:
        nav_hint.append("         ")
    nav_hint.append(f"  Halaman {position}/{total}  ", style="bold white on #1a1a2e")
    if position < total:
        nav_hint.append("  Next →", style="bold cyan")

    c.print(Align.center(nav_hint), style="")

    title_text = Text(f"  ✦  {node.title}  ✦  ", style="bold #f0e68c on #1a1a2e")
    c.print(
        Panel(
            Align.center(title_text),
            box=box.DOUBLE_EDGE,
            style="#4a90d9",
            padding=(0, 2),
        )
    )

    # ── Tabel Data ───────────────────────────────────────────────────
    table = Table(
        box=box.SIMPLE_HEAVY,
        header_style="bold #00d4ff on #0d1b2a",
        border_style="#2e4057",
        row_styles=["#d0d0d0", "#b0b8c4"],
        show_lines=False,
        expand=True,
    )

    for col in node.columns:
        table.add_column(col, justify="left", min_width=12)

    for i, row in enumerate(node.rows):
        if i == selected_row:
            # Baris terpilih: highlight kuning
            styled = [f"[bold #1a1a1a on #f0e68c]{cell}[/]" for cell in row]
            table.add_row(*styled)
        else:
            table.add_row(*[str(cell) for cell in row])

    c.print(table)

    # ── Footer navigasi ──────────────────────────────────────────────
    footer = Text()
    footer.append("↑↓", style="bold #00d4ff")
    footer.append(" pilih baris   ", style="#888")
    footer.append("←→", style="bold #00d4ff")
    footer.append(" ganti halaman   ", style="#888")
    footer.append("q", style="bold red")
    footer.append(" keluar", style="#888")
    c.print(Align.center(footer))

    return buf.getvalue()


# ─────────────────────────────────────────────
#  DATA CONTOH
# ─────────────────────────────────────────────


def build_carousel() -> TableCarousel:
    carousel = TableCarousel()

    carousel.append(
        title="📦  Inventaris Produk",
        columns=["ID", "Nama Produk", "Stok", "Harga (Rp)", "Kategori"],
        rows=[
            ["P001", "Laptop Asus A14", "12", "8.500.000", "Elektronik"],
            ["P002", "Mouse Logitech M185", "45", "120.000", "Aksesoris"],
            ["P003", "Keyboard Mechanical", "8", "650.000", "Aksesoris"],
            ["P004", 'Monitor LG 24"', "5", "2.100.000", "Elektronik"],
            ["P005", "Headset Sony WH-1000", "20", "3.200.000", "Audio"],
            ["P006", "Webcam Logitech C920", "15", "950.000", "Aksesoris"],
        ],
    )

    carousel.append(
        title="👥  Data Karyawan",
        columns=["NIP", "Nama", "Divisi", "Jabatan", "Status"],
        rows=[
            ["K001", "Andi Saputra", "IT", "Backend Dev", "Aktif"],
            ["K002", "Budi Hartono", "Finance", "Akuntan", "Aktif"],
            ["K003", "Citra Dewi", "HR", "Recruiter", "Cuti"],
            ["K004", "Deni Firmansyah", "IT", "DevOps", "Aktif"],
            ["K005", "Eka Rahayu", "Marketing", "Copywriter", "Aktif"],
        ],
    )

    carousel.append(
        title="📊  Laporan Penjualan Q1",
        columns=["Bulan", "Target (Rp)", "Realisasi (Rp)", "Selisih", "%"],
        rows=[
            ["Januari", "50.000.000", "47.300.000", "-2.700.000", "94.6%"],
            ["Februari", "55.000.000", "58.100.000", "+3.100.000", "105.6%"],
            ["Maret", "60.000.000", "61.500.000", "+1.500.000", "102.5%"],
            ["Total", "165.000.000", "166.900.000", "+1.900.000", "101.2%"],
        ],
    )

    carousel.append(
        title="🌐  Daftar Server",
        columns=["Hostname", "IP", "OS", "CPU", "Uptime"],
        rows=[
            ["prod-web-01", "10.0.1.10", "Ubuntu 22.04", "8 core", "99.9%"],
            ["prod-db-01", "10.0.1.20", "Debian 12", "16 core", "99.7%"],
            ["staging-01", "10.0.2.10", "Ubuntu 22.04", "4 core", "98.1%"],
            ["dev-01", "10.0.3.10", "Rocky Linux 9", "4 core", "95.3%"],
            ["backup-01", "10.0.4.10", "CentOS 7", "2 core", "99.5%"],
        ],
    )

    return carousel


# ─────────────────────────────────────────────
#  APLIKASI UTAMA
# ─────────────────────────────────────────────


def main():
    carousel = build_carousel()
    state = {"selected_row": 0}

    # ── Key Bindings ─────────────────────────────────────────────────
    kb = KeyBindings()

    @kb.add("right")
    def _(event):
        carousel.go_next()
        state["selected_row"] = 0  # reset pilihan baris
        event.app.invalidate()

    @kb.add("left")
    def _(event):
        carousel.go_prev()
        state["selected_row"] = 0
        event.app.invalidate()

    @kb.add("down")
    def _(event):
        max_row = len(carousel.current.rows) - 1
        if state["selected_row"] < max_row:
            state["selected_row"] += 1
        event.app.invalidate()

    @kb.add("up")
    def _(event):
        if state["selected_row"] > 0:
            state["selected_row"] -= 1
        event.app.invalidate()

    @kb.add("q")
    @kb.add("c-c")
    def _(event):
        event.app.exit()

    # ── Layout ───────────────────────────────────────────────────────
    def get_content():
        ansi_str = render_table(
            node=carousel.current,
            selected_row=state["selected_row"],
            position=carousel.position(),
            total=carousel.size,
            width=90,
        )
        return ANSI(ansi_str)

    layout = Layout(Window(content=FormattedTextControl(get_content), wrap_lines=False))

    # ── Application ──────────────────────────────────────────────────
    app = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True,
        mouse_support=False,
        color_depth=None,  # auto-detect terminal color support
    )

    app.run()
    print("\n✅  Keluar dari Table Carousel. Sampai jumpa!\n")


if __name__ == "__main__":
    main()
