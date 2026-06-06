"""
Demo Monitoring Server — Circular Linked List + Rich Live Table
@author: Abdullah Affandi

Setiap beberapa detik, vulnerable sebuah server di-toggle secara acak.
Data hasil toggle disimpan sementara ke tempfile.TemporaryFile
(tanpa menyentuh file JSON asli). Perubahan ditampilkan di log.
"""

import json
import random
import tempfile
import time
from pathlib import Path

from rich import box
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

DATA_PATH = Path("src/data/dalam-json/akun_dan_status_server.json")


# ── Circular Linked List ────────────────────────────────────────────


class CircularServerNode:
    """Node dalam circular singly linked list."""

    def __init__(
        self,
        *,
        server_id: str,
        server_name: str,
        ip: str,
        bandwidth_mbps: int,
        status: str,
        access: str,
        vulnerable: bool,
        credential: dict,
    ) -> None:
        self.server_id = server_id
        self.server_name = server_name
        self.ip = ip
        self.bandwidth_mbps = bandwidth_mbps
        self.status = status
        self.access = access
        self.vulnerable = vulnerable
        self.credential = credential
        self.next: "CircularServerNode | None" = None


class CircularServerMonitor:
    """Circular singly linked list untuk monitoring server."""

    def __init__(self) -> None:
        self.tail: CircularServerNode | None = None
        self.current: CircularServerNode | None = None
        self._count = 0

    @property
    def is_empty(self) -> bool:
        return self.tail is None

    @property
    def count(self) -> int:
        return self._count

    def add_server(
        self,
        *,
        server_id: str,
        server_name: str,
        ip: str,
        bandwidth_mbps: int,
        status: str,
        access: str,
        vulnerable: bool,
        credential: dict,
    ) -> None:
        node = CircularServerNode(
            server_id=server_id,
            server_name=server_name,
            ip=ip,
            bandwidth_mbps=bandwidth_mbps,
            status=status,
            access=access,
            vulnerable=vulnerable,
            credential=credential,
        )

        if self.is_empty:
            self.tail = node
            self.tail.next = node
            self.current = node
        else:
            node.next = self.tail.next
            self.tail.next = node
            self.tail = node

        self._count += 1

    def move_next(self) -> None:
        """Geser pointer current ke node berikutnya (round-robin)."""
        if self.current is not None:
            self.current = self.current.next

    def load_from_json(self, file_path: Path) -> None:
        """Muat data server dari file JSON ke dalam circular list."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for server in data["servers"]:
            self.add_server(
                server_id=server["server_id"],
                server_name=server["server_name"],
                ip=server["ip"],
                bandwidth_mbps=server["bandwidth_mbps"],
                status=server["status"],
                access=server["access"],
                vulnerable=server["vulnerable"],
                credential=server["credential"],
            )

    def to_dict_list(self) -> list[dict]:
        """Ekspor seluruh circular list ke list of dict (untuk serialisasi)."""
        if self.is_empty:
            return []

        result: list[dict] = []
        start = self.tail.next
        current = start

        while True:
            result.append(
                {
                    "server_id": current.server_id,
                    "server_name": current.server_name,
                    "ip": current.ip,
                    "bandwidth_mbps": current.bandwidth_mbps,
                    "status": current.status,
                    "access": current.access,
                    "vulnerable": current.vulnerable,
                    "credential": current.credential,
                }
            )
            current = current.next
            if current == start:
                break

        return result

    def toggle_random_vulnerable(self) -> tuple[CircularServerNode | None, bool | None]:
        """Pilih server acak dan toggle field vulnerable-nya.

        Returns:
            (node_yang_diubah, nilai_vulnerable_sebelum_toggle)
        """
        if self.is_empty:
            return None, None

        idx = random.randint(0, self._count - 1)

        start = self.tail.next
        current = start
        for _ in range(idx):
            current = current.next

        old_value = current.vulnerable
        current.vulnerable = not current.vulnerable

        return current, old_value


# ── Tampilan Rich ───────────────────────────────────────────────────


def _status_style(status: str) -> str:
    """Kembalikan Rich style string berdasarkan status server."""
    styles = {
        "ONLINE": "bold green",
        "OFFLINE": "dim",
        "MAINTENANCE": "bold yellow",
        "OVERLOAD": "bold red",
        "BLOCKED": "bold magenta",
    }
    return styles.get(status, "white")


def build_table(
    monitor: CircularServerMonitor,
    *,
    changed_server_id: str | None = None,
) -> Table:
    """Bangun Rich Table yang menampilkan seluruh server dalam circular list."""
    table = Table(
        title="SERVER MONITORING — CIRCULAR LINKED LIST",
        box=box.SIMPLE_HEAVY,
        show_lines=False,
    )

    table.add_column("Server ID", style="bold cyan", justify="center")
    table.add_column("Name", style="bold white")
    table.add_column("IP", style="white")
    table.add_column("Bandwidth", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Vulnerable", justify="center")

    if monitor.is_empty:
        return table

    start = monitor.tail.next
    current = start

    while True:
        vid = current.server_id

        if current.vulnerable:
            vuln_text = "[bold red]⚠ YES[/bold red]"
        else:
            vuln_text = "[green]✓ NO[/green]"

        status_str = current.status
        sstyle = _status_style(status_str)

        # Highlight baris yang baru berubah
        row_style = "on dark_red bold white" if vid == changed_server_id else None

        table.add_row(
            vid,
            current.server_name,
            current.ip,
            f"{current.bandwidth_mbps:,} Mbps",
            f"[{sstyle}]{status_str}[/{sstyle}]",
            vuln_text,
            style=row_style,
        )

        current = current.next
        if current == start:
            break

    return table


def build_info_panel(monitor: CircularServerMonitor) -> Panel:
    """Panel informasi: jumlah server, TemporaryFile, circular pointer."""
    info = Text()
    info.append("🔄 Circular List — ", style="bold cyan")
    info.append(f"{monitor.count} server termonitor. ", style="white")
    info.append("Data snapshot disimpan ke ", style="white")
    info.append("tempfile.TemporaryFile", style="bold magenta")
    info.append(" (file asli tidak diubah).", style="white")

    if monitor.current is not None:
        info.append(
            f"\n📍 Pointer saat ini: [{monitor.current.server_id}] {monitor.current.server_name}",
            style="bold cyan",
        )

    return Panel(info, border_style="blue")


# ── Main Loop ───────────────────────────────────────────────────────


def run_monitor(delay: float = 3.0) -> None:
    """Jalankan monitoring server dengan Live table."""
    monitor = CircularServerMonitor()
    monitor.load_from_json(DATA_PATH)

    change_log: list[str] = []
    max_log_entries = 6

    try:
        with Live(
            build_table(monitor),
            console=console,
            refresh_per_second=4,
            screen=False,
        ) as live:
            while True:
                # 1. Toggle vulnerable server acak
                changed_node, old_value = monitor.toggle_random_vulnerable()

                changed_id: str | None = None
                if changed_node is not None:
                    changed_id = changed_node.server_id

                    # 2. Tulis snapshot ke TemporaryFile (tanpa sentuh file asli)
                    with tempfile.TemporaryFile(
                        mode="w+", encoding="utf-8", suffix=".json"
                    ) as tmp:
                        snapshot = {"servers": monitor.to_dict_list()}
                        json.dump(snapshot, tmp, indent=2)
                        tmp.flush()
                        # Baca kembali untuk verifikasi
                        tmp.seek(0)
                        _verified = json.load(tmp)

                    # 3. Catat perubahan ke log
                    if changed_node.vulnerable:
                        arrow = "NO → [bold red]YES[/bold red] ⚠"
                    else:
                        arrow = "YES → [green]NO[/green] ✓"

                    note = (
                        f"[{changed_node.server_id}] {changed_node.server_name}: "
                        f"vulnerable {arrow}"
                    )
                    change_log.append(note)
                    if len(change_log) > max_log_entries:
                        change_log.pop(0)

                # 4. Susun tampilan
                table = build_table(monitor, changed_server_id=changed_id)

                if change_log:
                    log_text = "\n".join(change_log)
                else:
                    log_text = "[dim]Menunggu perubahan vulnerable...[/dim]"

                log_panel = Panel(
                    log_text,
                    title="📋 LOG PERUBAHAN VULNERABLE",
                    border_style="yellow",
                )

                info_panel = build_info_panel(monitor)

                content = Group(table, "", log_panel, "", info_panel)
                live.update(content)

                # 5. Geser pointer circular
                monitor.move_next()

                time.sleep(delay)

    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring dihentikan.[/yellow]")


if __name__ == "__main__":
    run_monitor(delay=3)
