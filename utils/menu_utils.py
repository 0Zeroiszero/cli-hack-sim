"""
@author: Abdullah Affandi
"""

from questionary import Style, Question
import questionary

from rich.console import Group
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel


def make_menu_selection_question(
    *,
    question: list[str | int],
    value: list[str | int],
    shortcut_key: str | None = None,
    use_shortcuts: bool = True,
    style: Style | None = None,
) -> Question:
    """
    Membuat pertanyaan berdasarkan question dan value sebagai nilai yang digunakan.
    Style merujuk kepada @questionary.Style yang digunakan untuk mengubah tampilan pertanyaan.
    Jika tidak ada parameter Style, maka default akan digunakan.
    Return merupakan questionary.Question

    Args:
        question: list[str | int] -> Pertanyaan yang akan ditampilkan, bisa berupa string atau integer.
        value: list[str | int] -> Nilai yang akan digunakan untuk pertanyaan.
        shortcut_key: str | None -> Key awalan yang akan digunakan untuk shortcut.
            Jika None, shortcut otomatis dibuat berdasarkan nomor urut.
            Contoh: "a" menghasilkan a1, a2, a3, dst.
        use_shortcuts: bool -> Mengaktifkan atau mematikan shortcut pada menu.
        style: Style | None -> Style yang akan digunakan untuk mengubah tampilan pertanyaan.

    Returns:
        Question -> Pertanyaan yang sudah dibuat berdasarkan parameter yang diberikan.
    """
    default_style = Style(
        [
            ("qmark", "fg:#00ff00 bold"),
            ("question", "fg:#ffffff bold"),
            ("answer", "fg:#00ff00 italic"),
            ("pointer", "fg:#00ff00 bold"),
            ("highlighted", "fg:#000000 bg:#00ff00 bold"),
            ("selected", "fg:#ff0033 bold"),
            ("separator", "fg:#333333"),
            ("instruction", "fg:#00aa00 italic"),
            ("text", "fg:#00ff00"),
            ("disabled", "fg:#444444 italic"),
        ]
    )

    if question is None:
        raise ValueError("Question tidak boleh None")

    if value is None:
        raise ValueError("Value tidak boleh None")

    if len(question) != len(value):
        raise ValueError("Panjang question dan value harus sama")

    if not isinstance(use_shortcuts, bool):
        raise ValueError("use_shortcuts harus berupa boolean")

    if shortcut_key is not None and not isinstance(shortcut_key, str):
        raise ValueError("shortcut_key harus berupa string atau None")

    choices = []

    for index, (question_item, value_item) in enumerate(zip(question, value), start=1):
        if not isinstance(question_item, (str, int)):
            raise ValueError("Question harus berupa string atau integer")

        if not isinstance(value_item, (str, int)):
            raise ValueError("Value harus berupa string atau integer")

        if use_shortcuts:
            current_shortcut = f"{shortcut_key}{index}" if shortcut_key else str(index)
        else:
            current_shortcut = None

        choices.append(
            questionary.Choice(
                title=str(question_item),
                value=value_item,
                shortcut_key=current_shortcut,
            )
        )

    q = questionary.select(
        "Pilih menu:",
        qmark="",
        choices=choices,
        default=0,
        use_shortcuts=use_shortcuts,
        style=style if style is not None else default_style,
        instruction="Gunakan arrow keys atau angka",
    )

    return q


def tampilkan_bandwidth_progress(
    *,
    rank: bool = False,
    data: list[tuple[int, str, str, int]],
) -> Panel:
    """
    Membuat panel daftar bandwidth server dalam bentuk progress bar Rich.

    Args:
        rank (bool): Jika True, tampilkan urutan ranking server.
        data (list[tuple[int, str, str, int]]): Daftar data bandwidth server.
            Format tuple:
            - index (int): Nomor urut/ranking server.
            - server_id (str): ID server.
            - server_name (str): Nama server.
            - bandwidth_mbps (int): Kecepatan bandwidth dalam satuan Mbps.

    Returns:
        Panel: Renderable Rich yang bisa digunakan untuk console.print() atau Live.
    """
    if not data:
        return Panel(
            "[bold red]Data bandwidth kosong.[/]",
            title="DAFTAR BANDWIDTH SERVER",
            border_style="red",
        )

    max_bandwidth = max(item[3] for item in data)

    progress_columns = []

    if rank:
        progress_columns.append(TextColumn("[white]{task.fields[rank]}[/]"))

    progress_columns.extend(
        [
            TextColumn("[white]{task.fields[server_id]}[/]"),
            TextColumn("[white]{task.fields[server_name]:<10}[/]"),
            BarColumn(
                bar_width=80,
                style="bright_black",
                complete_style="bright_blue",
                finished_style="bright_blue",
                pulse_style="bright_blue",
            ),
            TextColumn("[white]{task.completed:.0f} Mbps[/]"),
        ]
    )

    progress = Progress(
        *progress_columns,
        transient=False,
        expand=False,
    )

    for index, server_id, server_name, bandwidth in data:
        progress.add_task(
            description=server_name,
            total=max_bandwidth,
            completed=bandwidth,
            rank=f"[bold green][{index + 1}][/]",
            server_id=server_id,
            server_name=server_name,
        )

    return Panel(
        Group(progress),
        title="DAFTAR BANDWIDTH SERVER",
        border_style="green" if rank else "red",
    )
