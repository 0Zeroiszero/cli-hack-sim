"""
@author: Abdullah Affandi

Referensi ke DSA\stack
"""

from .stack import Stack

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class LogAktivitas(Stack):
    def __init__(self) -> None:
        super().__init__()
        self.console = Console()

    def add_log(self, message: str, *, value: int = 0) -> None:
        import datetime

        log_text = Text()
        waktu = datetime.datetime.now().strftime("%H:%M:%S")

        log_text.append(f"{waktu} | ", style="white")

        if value == 0:
            log_text.append("INFO", style="bold blue")
        elif value == 1:
            log_text.append("LOGIN", style="bold green")
        elif value == 2:
            log_text.append("ACTION", style="bold red")

        log_text.append(f" | {message}", style="white")

        self.push(log_text)

    def pop_log(self) -> None:
        if self.is_empty():
            self.console.print(Text("Log aktivitas masih kosong.", style="bold red"))

        self.pop()

    def clear_log(self) -> None:
        self.stack = []

    def peek(self) -> Text | None:
        if self.is_empty():
            return None
        return self.stack[-1]

    def peek_log(self) -> Text | None:
        if self.is_empty():
            self.console.print(Text("Log aktivitas masih kosong.", style="bold red"))
            return None

        return self.peek()

    def show_logs(self) -> None:
        if self.is_empty():
            self.console.print(
                Panel(
                    Text("Log aktivitas masih kosong.", style="bold red"),
                    title="LOG AKTIVITAS",
                    border_style="red",
                )
            )
            return

        log_text = Text(style="white")
        log_panel = Panel(
            log_text,
            title=f"LOG AKTIVITAS | TOTAL: {self.size()} AKTIVITAS",
            border_style="green",
        )

        items = list(reversed(self.stack))

        for index, item in enumerate(items):
            log_text.append_text(item)

            if index == 0:
                log_text.append("  <- TOP", style="bold yellow")

            if index != len(items) - 1:
                log_text.append("\n")

        self.console.print(log_panel)


if __name__ == "__main__":
    import time

    log = LogAktivitas()

    log.add_log("Test 1")
    time.sleep(1)

    log.add_log("Test 2")
    time.sleep(1)

    log.add_log("Test 3")
    time.sleep(1)

    log.add_log("Test 4")

    log.show_logs()

    log.pop_log()

    log.show_logs()
