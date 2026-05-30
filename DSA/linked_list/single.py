"""
@author: Abdullah Affandi
Implementasi Queue Traffic berdasarkan traffic.json
"""

from pathlib import Path
import time

# Rich guy
from rich.console import Console, Group
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich.spinner import Spinner

from src.filehandler import FileHandler
from DSA.queue.queue import Queue


# NOTE: Ini masuk ke menu [3]
# TODO: perbaiki Queue Size: N dengan return size [DONE MANIES]
class TrafficQueue(Queue):
    """
    TrafficQueue mewarisi Queue.

    Method asli dari Queue yang tetap dipakai:
    - enqueue()
    - dequeue()
    - front()
    - is_empty()
    - size()

    Method tambahan di class ini hanya untuk kebutuhan traffic:
    - load_from_json()
    - display()
    - display_front()
    - display_dequeue()
    """

    def __init__(self, file_path: str):
        super().__init__()
        self.fh = FileHandler()

        self.ph = Path(file_path)
        self.load_traffic()

        self.console = Console()

    def load_traffic(self) -> None:
        """
        Membaca traffic.json lalu memasukkan setiap request traffic ke queue.
        """

        traffic_data = self.fh.load_json(self.ph)

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

    # NOTE: Ini masuk ke menu [3.1] "Tampilkan Queue Traffic"
    def display(self) -> None:
        import random

        if self.is_empty():
            self.console.print(Text("   Queue traffic kosong.\n\n", style="bold red"))
            return

        rich_standard_color_list = self.fh.load_json(
            "utils/rich_standard_color_list.json"
        )
        nodes = []

        for index, item in enumerate(self.queue):
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
                f"method      : {metadata.get('method') or '-'}\n", style="cyan"
            )
            text.append(f"url         : {metadata.get('url') or '-'}\n", style="white")
            text.append(
                f"source      : {metadata.get('source') or '-'}\n", style="blue"
            )
            text.append(
                f"destination : {metadata.get('destination') or '-'}\n", style="blue"
            )
            text.append(
                f"protocol    : {metadata.get('protocol') or '-'}\n",
                style="bright_cyan",
            )
            text.append(
                f"status      : {metadata.get('status') or '-'}\n", style="yellow"
            )
            text.append(
                f"payload     : {metadata.get('payload') or '-'}\n", style="magenta"
            )
            text.append(
                f"latency     : {metadata.get('latency') or '-'}\n",
                style="bright_magenta",
            )

            nodes.append(
                Panel(
                    text,
                    title=f"Traffic {item['traffic_id']}",
                    border_style=panel_color,
                    width=32,
                )
            )

            if index != len(self.queue) - 1:
                nodes.append(
                    Align.center(
                        Text("──>", style="bold white"),
                        vertical="middle",
                    )
                )

        self.console.print(
            Columns(
                nodes,
                expand=False,
                equal=False,
            )
        )

    # NOTE: Ini masuk ke menu [3.2] "Lihat traffic terdepan"
    def display_front(self) -> None:
        if self.is_empty():
            self.console.print(Text("   Queue traffic kosong.\n\n", style="bold red"))
            return

        item = self.front()
        metadata = item["metadata"]

        text = Text()
        text.append(f"traffic_id  : {item['traffic_id']}\n", style="white")
        text.append(f"monitor_id  : {item['monitor_id']}\n", style="white")
        text.append(f"server_id   : {item['server_id']}\n", style="white")
        text.append(
            f"timestamp   : {metadata.get('timestamp') or '-'}\n", style="white"
        )
        text.append(f"method      : {metadata.get('method') or '-'}\n", style="white")
        text.append(f"url         : {metadata.get('url') or '-'}\n", style="white")
        text.append(f"source      : {metadata.get('source') or '-'}\n", style="white")
        text.append(
            f"destination : {metadata.get('destination') or '-'}\n", style="white"
        )
        text.append(f"protocol    : {metadata.get('protocol') or '-'}\n", style="white")
        text.append(f"status      : {metadata.get('status') or '-'}\n", style="white")
        text.append(f"payload     : {metadata.get('payload') or '-'}\n", style="white")
        text.append(f"latency     : {metadata.get('latency') or '-'}\n", style="white")
        text.append(
            f"threat_level: {metadata.get('threat_level') or '-'}", style="white"
        )

        self.console.print(
            Panel(
                text,
                title="TRAFFIC TERDEPAN",
                border_style="bold red",
                width=42,
            )
        )

    # NOTE: Ini masuk ke menu [3.2] "Proses Traffic Terdepan"
    def display_dequeue(self) -> None:
        if self.is_empty():
            self.console.print(Text("   Queue traffic kosong.\n\n", style="bold red"))
            return

        item = self.front()
        metadata = item["metadata"]

        def build_processing_panel(step_text: str, progress: float) -> Panel:
            info = Text(style="white")
            info.append(f"traffic_id   : {item['traffic_id']}\n")
            info.append(f"monitor_id   : {item['monitor_id']}\n")
            info.append(f"server_id    : {item['server_id']}\n")
            info.append(f"destination  : {metadata.get('destination')}\n")
            info.append(f"method       : {metadata.get('method') or '-'}\n")
            info.append(f"url          : {metadata.get('url') or '-'}\n")
            info.append(f"status       : {metadata.get('status') or '-'}\n")
            info.append(f"latency      : {metadata.get('latency') or '-'}\n\n")
            info.append(f"Step         : {step_text}\n", style="bold yellow")
            info.append(f"Progress     : {int(progress * 100)}%", style="bold green")

            return Panel(
                Group(
                    Spinner("dots", text=" Processing front traffic..."),
                    "",
                    info,
                ),
                title="MEMPROSES FRONT TRAFFIC",
                border_style="yellow",
                width=52,
            )

        steps = [
            "Mengambil data dari FRONT queue",
            "Membaca metadata traffic",
            "Memvalidasi request traffic",
            "Mengirim traffic ke proses berikutnya",
            "Menghapus item dari queue",
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

        is_failed = (removed_metadata.get("threat_level") or "").upper() == "HIGH"

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
        result_text.append(f"method      : {removed_metadata.get('method') or '-'}\n")
        result_text.append(f"url         : {removed_metadata.get('url') or '-'}\n")
        result_text.append(f"source      : {removed_metadata.get('source') or '-'}\n")
        result_text.append(
            f"destination : {removed_metadata.get('destination') or '-'}\n"
        )
        result_text.append(f"protocol    : {removed_metadata.get('protocol') or '-'}\n")
        result_text.append(f"status      : {removed_metadata.get('status') or '-'}\n")
        result_text.append(f"payload     : {removed_metadata.get('payload') or '-'}\n")
        result_text.append(f"latency     : {removed_metadata.get('latency') or '-'}\n")

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
            result_text.append("hasil       : BERHASIL\n\n", style="bold green")

        result_text.append(f"Sisa Queue  : {self.size()}", style="bold yellow")

        self.console.print(
            Panel(
                result_text,
                title=result_title,
                border_style=result_border,
                width=52,
            )
        )


if __name__ == "__main__":
    tf = TrafficQueue()

    tf.load_traffic()
    tf.display()
