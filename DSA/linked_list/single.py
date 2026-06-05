"""@author: Abdullah Affandi. 
Implementasi Queue Traffic berdasarkan traffic.json."""

import random
import time
from pathlib import Path

from rich.align import Align
from rich.columns import Columns

# Rich guy
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

from DSA.queue.queue import Queue
from src.filehandler import FileHandler


class TrafficNode:
    """Node untuk singly linked list traffic."""

    def __init__(self, data):
        """Inisialisasi node dengan data traffic."""
        self.data = data
        self.next = None

    @staticmethod
    def from_queue(queue_data):
        """Membangun linked list dari data queue 
        dan mengembalikan (head, rear)."""
        head = None
        rear = None

        for item in queue_data:
            new_node = TrafficNode(item)

            if head is None:
                head = new_node
                rear = new_node
            else:
                rear.next = new_node
                rear = new_node

        return head, rear


# NOTE: Ini masuk ke menu [3]
class TrafficQueue(Queue):
    """Queue traffic untuk membaca dan menampilkan data traffic dari JSON.

    Mewarisi Queue untuk operasi antrian (enqueue, dequeue, front, dll).
    Menggunakan TrafficNode untuk visualisasi dan traversal linked list.
    """

    def __init__(self, file_path: str):
        """Inisialisasi TrafficQueue dengan path file traffic JSON."""
        super().__init__()
        self.fh = FileHandler()

        self.ph = Path(file_path)
        self.console = Console()

        self.head_node = None
        self.rear_node = None
        self.current_node = None

        self.refresh_traffic()

    def refresh_traffic(self) -> None:
        """Memuat ulang data traffic dari file JSON."""
        self.queue.clear()
        self.load_traffic()

        self.head_node, self.rear_node = TrafficNode.from_queue(self.queue)
        self.current_node = self.head_node

    def load_traffic(self) -> None:
        """Membaca traffic.json dan memasukkan setiap request ke queue."""
        traffic_data = self.fh.load_json(self.ph)

        for server_name, monitors in traffic_data.items():
            for monitor_name, traffic_logs in monitors.items():
                for traffic in traffic_logs:
                    item = {
                        "traffic_id": traffic.get("request_id"),
                        "monitor_id": monitor_name,
                        "server_id": server_name,
                        "metadata": {
                            k: v
                            for k, v in traffic.items()
                            if k != "request_id"
                        },
                    }

                    self.enqueue(item)

    # NOTE: Ini masuk ke menu [3.1] "Tampilkan Queue Traffic"
    def display(self) -> None:
        """Menampilkan seluruh traffic dalam queue dengan format Columns."""
        if self.is_empty():
            self.console.print(
                Text("   Queue traffic kosong.\n\n", style="bold red")
            )
            return

        rich_standard_color_list = self.fh.load_json(
            "utils/rich_standard_color_list.json"
        )

        nodes = []

        current = self.head_node
        index = 0

        while current is not None:
            item = current.data
            metadata = item["metadata"]
            panel_color = random.choice(rich_standard_color_list)

            text = Text()
            text.append(f"monitor_id  : {item['monitor_id']}\n", style="green")
            text.append(f"server_id   : {item['server_id']}\n", style="green")
            text.append(
                f"timestamp   : {metadata.get('timestamp') or '-'}\n",
                style="bright_black",
            )
            text.append(
                f"method      : {metadata.get('method') or '-'}\n",
                style="cyan",
            )
            text.append(
                f"source      : {metadata.get('source') or '-'}\n",
                style="blue",
            )
            text.append(
                f"destination : {metadata.get('destination') or '-'}\n",
                style="blue",
            )

            nodes.append(
                Panel(
                    text,
                    title=f"Traffic {item['traffic_id']}",
                    border_style=panel_color,
                    width=32,
                )
            )

            if current.next is not None:
                nodes.append(
                    Align.center(
                        Text("➜", style="bold white"),
                        vertical="middle",
                    )
                )

            current = current.next
            index += 1

        self.console.print(
            Columns(
                nodes,
                expand=False,
                equal=False,
            )
        )

    # NOTE: Ini masuk ke menu [3.2] "Lihat traffic terdepan"
    def display_front(self) -> None:
        """Menampilkan traffic terdepan dan node berikutnya."""
        if self.is_empty():
            self.console.print(
                Text("   Queue traffic kosong.\n\n", style="bold red")
            )
            return

        front_node = self.head_node
        next_node = self.head_node.next if self.head_node is not None else None

        def build_traffic_panel(node, title: str, border_style: str) -> Panel:
            if node is None:
                empty_text = Text(
                    "Tidak ada node berikutnya.", style="bold red"
                )

                return Panel(
                    empty_text,
                    title=title,
                    border_style=border_style,
                    width=42,
                )

            item = node.data
            metadata = item["metadata"]

            text = Text()
            text.append(f"traffic_id  : {item['traffic_id']}\n", style="white")
            text.append(f"monitor_id  : {item['monitor_id']}\n", style="white")
            text.append(f"server_id   : {item['server_id']}\n", style="white")
            text.append(
                f"timestamp   : {metadata.get('timestamp') or '-'}\n",
                style="white",
            )
            text.append(
                f"method      : {metadata.get('method') or '-'}\n",
                style="white",
            )
            text.append(
                f"source      : {metadata.get('source') or '-'}\n",
                style="white",
            )
            text.append(
                f"destination : {metadata.get('destination') or '-'}\n",
                style="white",
            )
            text.append(
                f"threat_level: {metadata.get('threat_level') or '-'}",
                style="white",
            )

            return Panel(
                text,
                title=title,
                border_style=border_style,
                width=42,
            )

        front_panel = build_traffic_panel(
            front_node,
            title="TRAFFIC TERDEPAN",
            border_style="bold red",
        )

        arrow = Align.center(
            Text("➜", style="bold white"),
            vertical="middle",
        )

        next_panel = build_traffic_panel(
            next_node,
            title="NEXT",
            border_style="bold cyan",
        )

        self.console.print(
            Columns(
                [
                    front_panel,
                    arrow,
                    next_panel,
                ],
                expand=False,
                equal=False,
            )
        )

    # NOTE: Ini masuk ke menu [3.2] "Proses Traffic Terdepan"
    def display_dequeue(self) -> None:
        """Memproses traffic terdepan 
        dengan animasi dan menampilkan hasil dequeue."""
        if self.is_empty() or self.head_node is None:
            self.console.print(
                Text("   Queue traffic kosong.\n\n", style="bold red")
            )
            return

        front_node = self.head_node
        next_node = front_node.next

        item = front_node.data
        metadata = item["metadata"]

        def build_processing_panel(step_text: str, progress: float) -> Panel:
            info = Text(style="white")
            info.append(f"traffic_id   : {item['traffic_id']}\n")
            info.append(f"monitor_id   : {item['monitor_id']}\n")
            info.append(f"server_id    : {item['server_id']}\n")
            info.append(
                f"destination  : {metadata.get('destination') or '-'}\n"
            )
            info.append(f"method       : {metadata.get('method') or '-'}\n")
            info.append(
                f"threat_level : {metadata.get('threat_level') or '-'}\n\n"
            )

            if next_node is not None:
                info.append("next_node    : ", style="bold cyan")
                info.append(
                    f"Traffic {next_node.data['traffic_id']}\n\n",
                    style="white",
                )
            else:
                info.append("next_node    : ", style="bold cyan")
                info.append("None\n\n", style="bold red")

            info.append(f"Step         : {step_text}\n", style="bold yellow")
            info.append(
                f"Progress     : {int(progress * 100)}%", style="bold green"
            )

            return Panel(
                Group(
                    Spinner("dots", text=" Processing front traffic..."),
                    "",
                    info,
                ),
                title="MEMPROSES TRAFFIC TERDEPAN",
                border_style="yellow",
                width=54,
            )

        steps = [
            "Mengambil data dari head_node",
            "Membaca metadata traffic",
            "Memvalidasi request traffic",
            "Mengirim traffic ke proses berikutnya",
            "Menggeser head_node ke node berikutnya",
        ]

        with Live(
            build_processing_panel(steps[0], 0),
            console=self.console,
            refresh_per_second=8,
            transient=False,
        ) as live:
            for index, step in enumerate(steps, start=1):
                live.update(build_processing_panel(step, index / len(steps)))
                time.sleep(0.45)

        removed_item = self.dequeue()
        removed_metadata = removed_item["metadata"]

        # Sinkronkan linked node setelah dequeue dari Queue
        self.head_node = next_node
        self.current_node = self.head_node

        if self.head_node is None:
            self.rear_node = None

        is_failed = (
            removed_metadata.get("threat_level") or ""
        ).upper() == "HIGH"

        result_text = Text(style="white")

        if is_failed:
            result_text.append(
                "Traffic gagal diproses karena threat_level HIGH.\n"
                "Item tetap dikeluarkan dari queue untuk isolasi.\n\n",
                style="bold red",
            )
            result_title = "DEQUEUE TRAFFIC - GAGAL"
            result_border = "red"
        else:
            result_text.append(
                "Traffic berhasil diproses dan dikeluarkan dari queue.\n\n",
                style="bold green",
            )
            result_title = "DEQUEUE TRAFFIC - BERHASIL"
            result_border = "green"

        result_text.append(f"traffic_id  : {removed_item['traffic_id']}\n")
        result_text.append(f"monitor_id  : {removed_item['monitor_id']}\n")
        result_text.append(f"server_id   : {removed_item['server_id']}\n")
        result_text.append(
            f"timestamp   : {removed_metadata.get('timestamp') or '-'}\n"
        )
        result_text.append(
            f"method      : {removed_metadata.get('method') or '-'}\n"
        )
        result_text.append(
            f"source      : {removed_metadata.get('source') or '-'}\n"
        )
        result_text.append(
            f"destination : {removed_metadata.get('destination') or '-'}\n"
        )

        if is_failed:
            result_text.append(
                f"threat_level: {removed_metadata.get('threat_level') or '-'}\n",
                style="bold red",
            )
            result_text.append("hasil       : GAGAL\n\n", style="bold red")
        else:
            result_text.append(
                f"threat_level: {removed_metadata.get('threat_level') or '-'}\n"
            )
            result_text.append(
                "hasil       : BERHASIL\n\n", style="bold green"
            )

        if self.head_node is not None:
            result_text.append("head_node   : ", style="bold cyan")
            result_text.append(
                f"Traffic {self.head_node.data['traffic_id']}\n",
                style="white",
            )
        else:
            result_text.append("head_node   : None\n", style="bold red")

        if self.rear_node is not None:
            result_text.append("rear_node   : ", style="bold cyan")
            result_text.append(
                f"Traffic {self.rear_node.data['traffic_id']}\n",
                style="white",
            )
        else:
            result_text.append("rear_node   : None\n", style="bold red")

        result_text.append(
            f"\nSisa Queue  : {self.size()}", style="bold yellow"
        )

        self.console.print(
            Panel(
                result_text,
                title=result_title,
                border_style=result_border,
                width=54,
            )
        )


if __name__ == "__main__":
    tf = TrafficQueue("traffic.json")

    tf.load_traffic()
    tf.display()
