"""
Demo Rich Progress Bar untuk menampilkan bandwidth server.
@author: Abdullah Affandi
"""

import random

from rich.console import Group
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn

data_bandwidth = [
    (0, "SRV005", "Echo", 9123),
    (1, "SRV004", "Delta", 4000),
    (2, "SRV001", "Alpha", 1000),
    (3, "SRV003", "Gamma", 980),
    (4, "SRV010", "Titan", 766),
    (5, "SRV008", "Orion", 573),
    (6, "SRV002", "Beta", 230),
    (7, "SRV007", "Hydra", 220),
    (8, "SRV006", "Falcon", 120),
    (9, "SRV009", "Phoenix", 90),
]

random.shuffle(data_bandwidth)


def tampilkan_bandwidth_progress(
    console, *, data: list[tuple[int, str, str, int]]
) -> None:
    """Display bandwidth data as a Rich progress bar panel.

    Args:
        console: Rich Console instance for output.
        data: List of tuples (index, server_id, server_name, bandwidth_mbps).

    Returns:
        None.
    """
    if not data:
        console.print("[bold red]Data bandwidth kosong.[/]")
        return

    max_bandwidth = max(item[3] for item in data)

    progress = Progress(
        TextColumn("[white]{task.fields[server_id]}[/]"),
        TextColumn("[white]{task.fields[server_name]:<10}[/]"),
        BarColumn(
            bar_width=60,
            style="bright_black",
            complete_style="bright_blue",
            finished_style="bright_blue",
            pulse_style="bright_blue",
        ),
        TextColumn("[white]{task.completed:.0f} Mbps[/]"),
        console=console,
        transient=False,
        expand=False,
    )

    for _, server_id, server_name, bandwidth in data:
        progress.add_task(
            description=server_name,
            total=max_bandwidth,
            completed=bandwidth,
            server_id=server_id,
            server_name=server_name,
        )

    console.print(
        Panel(
            Group(progress),
            title="DAFTAR BANDWIDTH SERVER",
            border_style="red",
        )
    )


if __name__ == "__main__":
    tampilkan_bandwidth_progress(data_bandwidth)
