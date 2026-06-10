import time
from typing import Optional
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align


class Node:
    """Node dalam circular linked list yang merepresentasikan server.

    Attributes:
        node_id: ID unik server.
        name: Nama server.
        status: Status server (ONLINE/OFFLINE).
        next: Pointer ke node berikutnya dalam circular list.
    """

    def __init__(self, node_id: str, name: str, status: str) -> None:
        """Inisialisasi node server.

        Args:
            node_id: ID unik server.
            name: Nama server.
            status: Status server (ONLINE/OFFLINE).
        """
        self.node_id = node_id
        self.name = name
        self.status = status
        self.next: Optional["Node"] = None


class CircularLinkedList:
    """Circular singly linked list untuk menyimpan node server.

    Attributes:
        head: Node pertama dalam circular list.
    """

    def __init__(self) -> None:
        """Inisialisasi circular linked list kosong."""
        self.head: Optional[Node] = None

    def append(self, node_id: str, name: str, status: str) -> None:
        """Menambahkan node baru ke akhir circular list.

        Args:
            node_id: ID unik server.
            name: Nama server.
            status: Status server (ONLINE/OFFLINE).
        """
        new_node = Node(node_id, name, status)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            return

        current = self.head
        while current.next != self.head:
            current = current.next

        current.next = new_node
        new_node.next = self.head


class MonitoringServerRing:
    """Monitoring server menggunakan circular linked list dengan tampilan Rich.

    Attributes:
        clist: Circular linked list yang menyimpan node server.
        current_node: Node yang sedang aktif/ditunjuk.
        step_count: Jumlah langkah perpindahan yang telah dilakukan.
    """

    def __init__(self, nodes_config: list[dict]) -> None:
        """Inisialisasi monitoring ring dari konfigurasi node.

        Args:
            nodes_config: List of dict dengan key 'id', 'name', 'status'.
        """
        self.clist = CircularLinkedList()
        for cfg in nodes_config:
            self.clist.append(cfg["id"], cfg["name"], cfg["status"])

        self.current_node = self.clist.head
        self.step_count = 0

    def move_next(self) -> None:
        """Memindahkan pointer current_node ke node berikutnya."""
        if self.current_node:
            self.current_node = self.current_node.next
            self.step_count += 1

    def generate_renderable(self) -> Panel:
        """Menghasilkan Panel Rich yang menampilkan visual circular list.

        Returns:
            Panel Rich berisi grid node server dengan pointer current,
            panah koneksi, dan informasi footer.
        """
        if not self.clist.head:
            return Panel("List is empty")

        nodes = []
        curr = self.clist.head
        while True:
            nodes.append(curr)
            curr = curr.next
            if curr == self.clist.head:
                break

        # We use a grid to precisely control the layout
        grid = Table.grid(expand=True)

        # Row 1: HEAD
        head_row = [Align.center(Text("HEAD", style="bold white"))]
        # Fill the rest of the row with empty cells to match node count
        head_row.extend([""] * (len(nodes) * 2))
        grid.add_row(*head_row)

        # Row 2: │
        pipe_row = [Align.center(Text("│", style="bold white"))]
        pipe_row.extend([""] * (len(nodes) * 2))
        grid.add_row(*pipe_row)

        # Row 3: ▼
        arrow_down_row = [Align.center(Text("▼", style="bold white"))]
        arrow_down_row.extend([""] * (len(nodes) * 2))
        grid.add_row(*arrow_down_row)

        # Row 4: The Nodes and their connecting arrows
        node_row = []
        for i, node in enumerate(nodes):
            is_active = node == self.current_node

            node_content = Text()
            node_content.append(
                f"{node.node_id}\n", style="bold" if is_active else "white"
            )
            node_content.append(f"{node.name}\n", style="white")
            node_content.append(
                f"{node.status}",
                style="green" if node.status == "ONLINE" else "red",
            )

            node_panel = Panel(
                node_content,
                border_style="bold yellow" if is_active else "white",
                expand=False,
                padding=(0, 2),
            )
            node_row.append(node_panel)

            if i < len(nodes) - 1:
                # Center the arrow vertically relative to the panel
                # Panel height is 5 lines, so 2 newlines puts arrow on line 3
                node_row.append(
                    Group(
                        Text("\n\n"), Align.center(Text("──▶", style="white"))
                    )
                )
            else:
                # Return arrow
                node_row.append(
                    Group(
                        Text("\n\n"),
                        Align.center(
                            Text(
                                "──▶ [bold magenta]Back to Head[/bold magenta]",
                                style="white",
                            )
                        ),
                    )
                )

        grid.add_row(*node_row)

        # Container for the grid and the footer
        container = Table.grid(expand=True)
        container.add_row(grid)

        footer = Text("\n")
        footer.append(
            f"  CURRENT: {self.current_node.node_id} / {self.current_node.name}\n",
            style="bold cyan",
        )
        footer.append(
            f"  STATUS : {self.current_node.status}", style="bold cyan"
        )
        container.add_row(footer)

        return Panel(
            container,
            title="[bold green]CIRCULAR LINKED LIST MONITORING[/bold green]",
            border_style="green",
            expand=False,
        )


def main() -> None:
    """Menjalankan demo monitoring server ring dengan Rich Live.

    Membuat 4 node server dalam circular linked list dan menampilkan
    visualisasi yang diperbarui setiap detik dengan perpindahan pointer.
    """
    nodes_config = [
        {"id": "SRV001", "name": "Alpha", "status": "ONLINE"},
        {"id": "SRV002", "name": "Beta", "status": "OFFLINE"},
        {"id": "SRV003", "name": "Gamma", "status": "ONLINE"},
        {"id": "SRV004", "name": "Delta", "status": "ONLINE"},
    ]

    ring = MonitoringServerRing(nodes_config)
    console = Console()

    with Live(
        ring.generate_renderable(), refresh_per_second=4, console=console
    ) as live:
        try:
            while True:
                time.sleep(1)
                ring.move_next()
                live.update(ring.generate_renderable())
        except KeyboardInterrupt:
            console.print("\n[bold red]Monitoring stopped by user.[/bold red]")


if __name__ == "__main__":
    main()
