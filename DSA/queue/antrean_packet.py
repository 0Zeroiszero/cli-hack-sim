'''
Referensi ke DSA\queue

'''

from .queue import Queue

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

class AntrianPacket(Queue):
    def __init__(self) -> None:
        super().__init__()
        self.console = Console()

    def show_queue(self) -> None:
        if self.is_empty():
            self.console.print(Text("Antrian packet masih kosong.", style="bold red"))
            return
        
        queue_text = Text(style="bold blue")
        queue_panel = Panel(queue_text, title=f"ANTRIAN PACKET | JUMLAH: {self.size()} ANTRIAN", style="bold blue")
        items = list(self.queue)

        for index, item in enumerate(items):
            queue_text.append(item)

            if index == 0:
                queue_text.append("  <- DEPAN", style="bold yellow")

            if index != len(items) - 1:
                queue_text.append("\n")
                
        self.console.print(queue_panel)
    
    def clear_queue(self) -> None:
        self.queue = []
    
    def peek_queue(self) -> object:
        if self.is_empty():
            self.console.print(Text("Antrian packet masih kosong.", style="bold red"))
            return None

        packet = self.front()
        self.console.print(Text(f"Packet '{packet}' berada di depan antrian.", style="bold green"))
        return packet
    
    def enqueue_packet(self, packet) -> None:
        self.enqueue(packet)
        self.console.print(Text(f"Packet '{packet}' telah ditambahkan ke antrian.", style="bold green"))

    def dequeue_packet(self) -> object:
        if self.is_empty():
            self.console.print(Text("Antrian packet masih kosong.", style="bold red"))
            return None

        packet = self.dequeue()
        self.console.print(Text(f"Packet '{packet}' telah dihapus dari antrian.", style="bold green"))
        return packet
    