"""
Demo TrafficQueue dengan Rich
@author: Abdullah Affandi
"""

import json

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.pretty import Pretty
from rich import box


console = Console()


class Queue:
    """
    Queue digunakan untuk menyimpan antrean paket.
    Bersifat FIFO (First In First Out).
    """

    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)

        raise IndexError("Queue is empty")

    def front(self):
        if not self.is_empty():
            return self.queue[0]

        raise IndexError("Queue is empty")

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


class TrafficQueue(Queue):
    def load_from_json(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as file:
            traffic_data = json.load(file)

        for server_name, monitors in traffic_data.items():
            for monitor_name, traffic_logs in monitors.items():
                for traffic in traffic_logs:
                    item = {
                        "traffic_id": traffic.get("request_id"),
                        "monitor_id": monitor_name,
                        "server_id": server_name,
                        "metadata": {
                            "timestamp": traffic.get("timestamp"),
                            "method": traffic.get("method"),
                            "url": traffic.get("url"),
                            "source": traffic.get("source"),
                            "destination": traffic.get("destination"),
                            "protocol": traffic.get("protocol"),
                            "status": traffic.get("status"),
                            "payload": traffic.get("payload"),
                            "latency": traffic.get("latency"),
                            "threat_level": traffic.get("threat_level"),
                        },
                    }

                    self.enqueue(item)

    def display(self) -> None:
        if self.is_empty():
            console.print("[bold red]Queue traffic kosong.[/bold red]")
            return

        table = Table(
            title="TRAFFIC QUEUE",
            box=box.SIMPLE_HEAVY,
            show_lines=False,
        )

        table.add_column("No", justify="center", style="bold cyan")
        table.add_column("Traffic ID", justify="center", style="bold green")
        table.add_column("Monitor ID", style="green")
        table.add_column("Server ID", style="green")
        table.add_column("Method", justify="center")
        table.add_column("URL")
        table.add_column("Status")
        table.add_column("Latency", justify="center")

        for index, item in enumerate(self.queue, start=1):
            metadata = item["metadata"]

            status = metadata.get("status")
            threat_level = metadata.get("threat_level")

            if threat_level == "HIGH":
                row_style = "bold red"
            elif status and "403" in status:
                row_style = "bold yellow"
            elif status and "500" in status:
                row_style = "bold red"
            else:
                row_style = None

            table.add_row(
                str(index),
                str(item["traffic_id"]),
                item["monitor_id"],
                item["server_id"],
                str(metadata.get("method")),
                str(metadata.get("url")),
                str(metadata.get("status")),
                str(metadata.get("latency")),
                style=row_style,
            )

        console.print(
            Panel(
                table,
                title="SINGLE LINKED LIST / QUEUE TRAFFIC",
                subtitle=f"Queue Size: {self.size()}",
                border_style="green",
            )
        )

    def display_front(self) -> None:
        if self.is_empty():
            console.print("[bold red]Queue traffic kosong.[/bold red]")
            return

        item = self.front()

        self._display_traffic_detail(
            item=item,
            title="FRONT TRAFFIC",
            subtitle="Data terdepan ditampilkan tanpa dihapus",
            border_style="cyan",
        )

    def display_dequeue(self) -> None:
        if self.is_empty():
            console.print("[bold red]Queue traffic kosong.[/bold red]")
            return

        item = self.dequeue()

        self._display_traffic_detail(
            item=item,
            title="DEQUEUE TRAFFIC",
            subtitle=f"Sisa Queue: {self.size()}",
            border_style="yellow",
        )

    def _display_traffic_detail(
        self,
        *,
        item: dict,
        title: str,
        subtitle: str,
        border_style: str,
    ) -> None:
        detail_table = Table(show_header=False, box=None)
        detail_table.add_column("Field", style="bold white")
        detail_table.add_column("Value", style="bold green")

        detail_table.add_row("Traffic ID", str(item["traffic_id"]))
        detail_table.add_row("Monitor ID", item["monitor_id"])
        detail_table.add_row("Server ID", item["server_id"])

        metadata_panel = Panel(
            Pretty(item["metadata"]),
            title="METADATA",
            border_style="blue",
        )

        content = Group(
            detail_table,
            "",
            metadata_panel,
        )

        console.print(
            Panel(
                content,
                title=title,
                subtitle=subtitle,
                border_style=border_style,
            )
        )


if __name__ == "__main__":
    traffic_queue = TrafficQueue()

    traffic_queue.load_from_json("src/data/dalam-json/traffic.json")

    traffic_queue.display()

    console.input("\n[bold cyan]Tekan Enter untuk melihat traffic terdepan...[/bold cyan]")
    traffic_queue.display_front()

    console.input("\n[bold cyan]Tekan Enter untuk memproses traffic terdepan...[/bold cyan]")
    traffic_queue.display_dequeue()