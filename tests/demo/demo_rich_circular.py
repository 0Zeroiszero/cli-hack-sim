"""
Demo Rich Live untuk Circular Linked List Monitoring
@author: Abdullah Affandi
"""

import time
<<<<<<< HEAD

=======
>>>>>>> main
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.server import Server

console = Console()


<<<<<<< HEAD
class CircularServerNode(Server):
    """A node in a circular linked list representing a server.

    Args:
        server_id: Unique server identifier.
        server_name: Human-readable server name.
        ip: IP address of the server.
        status: Current operational status.
        vulnerable: Whether the server is flagged as vulnerable.
        access: Access level (e.g. LOCKED).

    Returns:
        None.
    """

=======
"""class Server:
    def __init__(self, nama, id, ip, status):
        self.nama = nama
        self.id = id
        self.ip = ip
        self.status = status"""


class CircularServerNode(Server):
>>>>>>> main
    def __init__(
        self,
        *,
        server_id: str,
        server_name: str,
        ip: str,
        status: str,
        vulnerable: bool = False,
        access: str = "LOCKED",
    ):
        super().__init__(
            nama=server_name,
            id=server_id,
            ip=ip,
            status=status,
        )

        self.vulnerable = vulnerable
        self.access = access
        self.previous_status = status
        self.next = None


class CircularServerMonitoring:
<<<<<<< HEAD
    """Manages a circular linked list of servers and provides live monitoring.

    Args:
        None.

    Returns:
        None.
    """

=======
>>>>>>> main
    def __init__(self):
        self.tail = None
        self.current = None

    def is_empty(self):
<<<<<<< HEAD
        """Check whether the circular list is empty.

        Args:
            None.

        Returns:
            bool: True if the list has no nodes, False otherwise.
        """
=======
>>>>>>> main
        return self.tail is None

    def add_server(
        self,
        *,
        server_id: str,
        server_name: str,
        ip: str,
        status: str,
        vulnerable: bool = False,
        access: str = "LOCKED",
    ):
<<<<<<< HEAD
        """Add a new server node to the circular list.

        Args:
            server_id: Unique server identifier.
            server_name: Human-readable server name.
            ip: IP address of the server.
            status: Current operational status.
            vulnerable: Whether the server is flagged as vulnerable.
            access: Access level (e.g. LOCKED).

        Returns:
            None.
        """
=======
>>>>>>> main
        new_node = CircularServerNode(
            server_id=server_id,
            server_name=server_name,
            ip=ip,
            status=status,
            vulnerable=vulnerable,
            access=access,
        )

        if self.is_empty():
            self.tail = new_node
            self.tail.next = new_node
            self.current = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
            self.tail = new_node

    def move_next(self):
<<<<<<< HEAD
        """Advance the current pointer to the next node in the circular list.

        Args:
            None.

        Returns:
            None.
        """
=======
>>>>>>> main
        if self.current is not None:
            self.current = self.current.next

    def build_monitor_view(self):
<<<<<<< HEAD
        """Build a Rich Panel displaying the current server's monitoring data.

        Args:
            None.

        Returns:
            Panel: A Rich Panel with server details, change, and alert.
        """
=======
>>>>>>> main
        if self.current is None:
            return Panel(
                "[red]Belum ada server untuk dimonitor.[/red]",
                title="CIRCULAR LINKED LIST MONITOR",
                border_style="red",
            )

        changed = self.current.previous_status != self.current.status

        if changed:
            self.current.vulnerable = True
            self.current.previous_status = self.current.status

        if self.current.vulnerable:
            border_style = "red"
            value_style = "bold red"
            alert_text = Text("ALERT: SERVER VULNERABLE", style="bold red")
        else:
            border_style = "green"
            value_style = "bold green"
            alert_text = Text("ALERT: SERVER AMAN", style="bold green")

        table = Table(show_header=False, box=None)
        table.add_column("Field", style="bold white")
        table.add_column("Value", style=value_style)

        table.add_row("Server ID", self.current.id)
        table.add_row("Server Name", self.current.nama)
        table.add_row("IP Address", self.current.ip)
        table.add_row("Current Status", self.current.status)
        table.add_row("Previous Status", self.current.previous_status)
        table.add_row("Access", self.current.access)
        table.add_row("Vulnerable", str(self.current.vulnerable))

        if changed:
            change_text = Text(
                "CHANGE DETECTED\n"
                "Status berubah dari histori sebelumnya.\n"
                "Action: vulnerable otomatis menjadi True.",
                style="bold red",
            )
        else:
            change_text = Text(
                "CHANGE DETECTED\nTidak ada perubahan.",
                style="bold yellow",
            )

        content = Group(
            table,
            "",
            change_text,
            "",
            alert_text,
        )

        return Panel(
            content,
            title="CIRCULAR LINKED LIST MONITOR",
            subtitle="CTRL + C untuk berhenti",
            border_style=border_style,
        )

    def update_status_demo(self, server_id: str, new_status: str):
<<<<<<< HEAD
        """Update the status of a server by its ID for demo purposes.

        Args:
            server_id: The server identifier to update.
            new_status: The new status value to assign.

        Returns:
            bool: True if the server was found and updated, False otherwise.
        """
=======
>>>>>>> main
        if self.is_empty():
            return False

        start = self.tail.next
        current = start

        while True:
            if current.id == server_id:
                current.status = new_status
                return True

            current = current.next

            if current == start:
                break

        return False

    def run_auto_monitor(self, delay: float = 2):
<<<<<<< HEAD
        """Run an automatic live monitoring loop that cycles through servers.

        Args:
            delay: Seconds to wait between each server rotation.

        Returns:
            None.
        """
=======
>>>>>>> main
        try:
            with Live(
                self.build_monitor_view(),
                console=console,
                refresh_per_second=3,
                screen=False,
            ) as live:
                counter = 0

                while True:
                    live.update(self.build_monitor_view())

                    counter += 1

<<<<<<< HEAD
=======
                    # Demo perubahan status otomatis
                    # Setelah beberapa putaran, SRV003 berubah status.
>>>>>>> main
                    if counter == 5:
                        self.update_status_demo("SRV003", "OFFLINE")

                    self.move_next()
                    time.sleep(delay)

        except KeyboardInterrupt:
            console.print("\n[yellow]Monitoring dihentikan.[/yellow]")


if __name__ == "__main__":
    monitor = CircularServerMonitoring()

    monitor.add_server(
        server_id="SRV001",
        server_name="Server Alpha",
        ip="192.168.1.10",
        status="ONLINE",
    )

    monitor.add_server(
        server_id="SRV002",
        server_name="Server Beta",
        ip="192.168.1.20",
        status="ONLINE",
    )

    monitor.add_server(
        server_id="SRV003",
        server_name="Server Gamma",
        ip="192.168.1.30",
        status="ONLINE",
    )

    monitor.add_server(
        server_id="SRV004",
        server_name="Server Delta",
        ip="192.168.1.40",
        status="OFFLINE",
    )

    monitor.run_auto_monitor(delay=1.5)
