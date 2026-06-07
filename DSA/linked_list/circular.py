"""Modul circular linked list untuk monitoring server.

Menyediakan kelas CircularServerNode yang membangun circular
singly linked list dari data server untuk keperluan monitoring
dan visualisasi live.

@author: Abdullah Affandi
"""

import random
import time
from pathlib import Path
from typing import cast

from rich import box
from rich.console import Console
from rich.live import Live
from rich.table import Table

from src import FileHandler, ServerNode


class CircularServerNode(ServerNode):
    """Node server yang terhubung secara circular (singly linked list).

    Setelah inisialisasi, seluruh node terhubung membentuk lingkaran
    di mana node terakhir (tail) mengarah kembali ke node pertama (head).

    Attributes:
        vulnerable: Status kerentanan server (True jika rentan).
        next: Pointer ke node berikutnya dalam circular list.
        current: Pointer ke node yang sedang aktif/diproses.

    """

    def __init__(self, data: dict) -> None:
        """Bangun circular linked list dari data server JSON.

        Args:
            data: Dictionary hasil load_json yang berisi key "servers"
                  dengan daftar server.

        """
        servers: list[dict] = data["servers"]

        first = servers[0]
        super().__init__(
            nama=first["server_name"],
            id=first["server_id"],
            ip=first["ip"],
            status=first["status"],
        )
        self.vulnerable: bool = first.get("vulnerable", False)
        self.next: CircularServerNode | None = None

        self.current = self
        for server in servers[1:]:
            node = object.__new__(CircularServerNode)
            ServerNode.__init__(
                node,
                nama=server["server_name"],
                id=server["server_id"],
                ip=server["ip"],
                status=server["status"],
            )
            node.vulnerable = server.get("vulnerable", False)
            self.current.next = node
            self.current = node

        self.current.next = self
        self.current = self

    def _make_random_server_vulnerable(
        self,
        target: CircularServerNode,
    ) -> None:
        """Mengubah status vulnerable target secara acak.

        Jika angka random 1-9 bernilai genap, status vulnerable
        target akan di-toggle (dibalik).

        Args:
            target: Node server yang akan diubah statusnya.

        """
        angka = random.randint(1, 9)
        if angka % 2 != 0:
            return
        target.vulnerable = not target.vulnerable

    def _collect_all_nodes(self) -> list["CircularServerNode"]:
        """Mengumpulkan seluruh node dari circular linked list.

        Returns:
            list[CircularServerNode]: Daftar semua node dalam circular list.

        """
        nodes: list[CircularServerNode] = []
        node = self
        while True:
            nodes.append(node)
            node = cast("CircularServerNode", node.next)
            if node is self:
                break
        return nodes

    def _advance_current(self) -> None:
        """Maju satu langkah ke node berikutnya (circular)."""
        assert self.current.next is not None  # noqa: S101
        self.current = self.current.next

    def _build_monitoring_table(
        self,
        highlight_id: str | None = None,
    ) -> Table:
        """Membangun tabel monitoring seluruh server dalam circular list.

        Args:
            highlight_id: Server ID yang akan diberi highlight khusus.

        Returns:
            Table: Rich Table yang menampilkan status seluruh server.

        """
        table = Table(border_style="green", box=box.HORIZONTALS, expand=True)
        table.add_column("Server ID", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("IP", style="yellow")
        table.add_column("Status")
        table.add_column("Vulnerable")

        node = self
        while True:
            status_upper = node.status.strip().upper()
            status_color = {
                "ONLINE": "green",
                "OFFLINE": "red",
                "MAINTENANCE": "yellow",
                "BLOCKED": "red",
                "OVERLOAD": "magenta",
            }.get(status_upper, "white")

            if node.id == highlight_id:
                if node.vulnerable:
                    row_style = "on red"
                    vuln_text = "[bold white]YES[/bold white]"
                else:
                    row_style = "on white"
                    vuln_text = "[bold black]NO[/bold black]"
            elif node.vulnerable:
                row_style = "on red"
                vuln_text = "[bold white]YES[/bold white]"
            else:
                row_style = ""
                vuln_text = "[green]NO[/green]"

            table.add_row(
                node.id,
                node.nama,
                node.ip,
                f"[{status_color}]{node.status}[/{status_color}]",
                vuln_text,
                style=row_style,
            )
            node = cast("CircularServerNode", node.next)
            if node is self:
                break

        return table

    def _make_circular_live_table(self) -> None:
        """Menampilkan live monitoring server circular.

        Menampilkan tabel yang diperbarui secara real-time dengan
        efek "satpam putih" yang berkeliling memulihkan server merah
        (vulnerable) menjadi normal.
        """
        console = Console()
        nodes = self._collect_all_nodes()

        console.print("[dim]Tekan Ctrl+C untuk berhenti...[/dim]")
        try:
            with Live(
                self._build_monitoring_table(),
                refresh_per_second=4,
                console=console,
            ) as live:
                while True:
                    time.sleep(0.25)

                    if random.randint(1, 4) == 1:
                        target = random.choice(nodes)
                        self._make_random_server_vulnerable(target)

                    self._advance_current()

                    if self.current.vulnerable:
                        self.current.vulnerable = False

                    live.update(
                        self._build_monitoring_table(self.current.id),
                    )
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    raw_data = FileHandler().load_json(
        Path("data/dalam-json/akun_dan_status_server.json"),
    )
    assert isinstance(raw_data, dict)  # noqa: S101
    head = CircularServerNode(raw_data)

    print("\n--- Live Monitoring ---")
    head._make_circular_live_table()
