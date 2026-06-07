"""
@author: Abdullah Affandi
"""

import time
from ipaddress import IPv4Address, AddressValueError

from src import FileHandler

from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit import prompt

import questionary
from questionary import Style, Question
from rich.console import Console, Group
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich.status import Status
from rich.text import Text
from rich.table import Table
from rich import box


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


def display_search_ip_result(
    *, result: list[tuple[int, str, str, str, str, bool]]
) -> Panel:
    """
    Membuat tampilan hasil pencarian alamat IP server dalam bentuk Rich Panel.

    Parameter result berisi daftar tuple hasil pencarian server dengan format:
    (index, ip, server_id, server_name, status, found)

    Keterangan tuple:
    - index: urutan data server.
    - ip: alamat IP server.
    - server_id: ID server.
    - server_name: nama server.
    - status: status server, misalnya ONLINE, OFFLINE, MAINTENANCE, BLOCKED, atau OVERLOAD.
    - found: penanda apakah server tersebut cocok dengan IP yang dicari.

    Baris yang memiliki found bernilai True akan ditampilkan lebih terang dan
    diberi label "--- FOUND". Status server juga diberi warna sesuai kondisinya.

    Returns:
        Panel: Rich Panel berisi daftar hasil pencarian IP yang siap ditampilkan
        menggunakan console.print().
    """
    try:
        body = Text()
        found = False

        for index, ip, server_id, server_name, status, found in result:
            status_style = {
                "ONLINE": "bold green",
                "OFFLINE": "bold red",
                "MAINTENANCE": "bold yellow",
                "BLOCKED": "bold red",
                "OVERLOAD": "bold magenta",
            }.get(status, "white")
            if found:
                body.append(f"[{index + 1}] ", style="bold bright_white")
                body.append(f"{ip:<14} ", style="bold bright_cyan")
                body.append("| ", style="bold bright_white")
                body.append(f"Server {server_name:<8} ", style="bold bright_white")
                body.append("| ", style="bold bright_white")
                body.append(f"{status:<11}", style=status_style)
                body.append(" --- FOUND", style="bold bright_yellow")
                body.append("\n")

                # Kalau ketemu
                found = True
            else:
                body.append(f"[{index + 1}] ", style="white")
                body.append(f"{ip:<14} ", style="cyan")
                body.append("| ", style="white")
                body.append(f"Server {server_name:<8} ", style="white")
                body.append("| ", style="white")
                body.append(f"{status:<11}", style=status_style)
                body.append("\n")

        c = Console()
        status = Status("[bold green]Mencari alamat IP...", console=c)

        with Live(status, refresh_per_second=10):
            time.sleep(1.5)
            if found:
                status.update("[bold green]Alamat IP ditemukan...")
                time.sleep(1.5)
            else:
                status.update("[bold red]Alamat IP tidak ditemukan...")
                time.sleep(1.5)

        return Panel(
            body,
            title="MENCARI ALAMAT IP",
            title_align="center",
            border_style="green" if found else "red",
        )
    except TypeError:
        return False


def make_traversal_folder(
    pilihan_traversal: str = "preorder",
    preorder: str = "",
    inorder: str = "",
    postorder: str = "",
) -> tuple[Panel, Table]:
    """
    Membuat Panel dan Table Rich berdasarkan traversal yang dipilih.

    Args:
        pilihan_traversal (str): Traversal utama yang ditampilkan di Panel.
            Pilihan: "preorder", "inorder", atau "postorder".
        preorder (str): Hasil traversal preorder.
        inorder (str): Hasil traversal inorder.
        postorder (str): Hasil traversal postorder.

    Returns:
        tuple[Panel, Table]: Panel traversal utama dan tabel traversal lainnya.
    """

    if pilihan_traversal == "preorder":
        tree_text = preorder
        panel_title = "Preorder Tree"

        row_1_name = "Inorder"
        row_1_value = inorder
        row_1_style = "dark_red"

        row_2_name = "Postorder"
        row_2_value = postorder
        row_2_style = "white"

    elif pilihan_traversal == "inorder":
        tree_text = inorder
        panel_title = "Inorder Tree"

        row_1_name = "Preorder"
        row_1_value = preorder
        row_1_style = "dark_red"

        row_2_name = "Postorder"
        row_2_value = postorder
        row_2_style = "white"

    elif pilihan_traversal == "postorder":
        tree_text = postorder
        panel_title = "Postorder Tree"

        row_1_name = "Preorder"
        row_1_value = preorder
        row_1_style = "dark_red"

        row_2_name = "Inorder"
        row_2_value = inorder
        row_2_style = "white"

    else:
        tree_text = preorder
        panel_title = "Preorder Tree"

        row_1_name = "Inorder"
        row_1_value = inorder
        row_1_style = "dark_red"

        row_2_name = "Postorder"
        row_2_value = postorder
        row_2_style = "white"

    panel = Panel(tree_text, title=panel_title, border_style="green")

    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="white",
        box=box.SIMPLE,
        expand=True,
        padding=(1, 2),
    )

    table.add_column("Traversal Lainnya", style="bold green", no_wrap=True)
    table.add_column("Hasil", style="white")

    table.add_row(Text(row_1_name, style=row_1_style), Text(row_1_value))
    table.add_row(Text(row_2_name, style=row_2_style), Text(row_2_value))

    return (panel, table)


def ask_for_server(prompt_text: str = "Pilih Server: ") -> str | None:
    """Meminta input server ID dengan autocomplete format 'SRV001 - Alpha'.

    Args:
        prompt_text: Teks yang ditampilkan saat meminta input.

    Returns:
        str: Server ID (contoh: "SRV001"), atau None jika gagal.
    """
    from pathlib import Path

    from src.filehandler import FileHandler

    server_data = FileHandler().load_json(
        Path("src/data/dalam-json/akun_dan_status_server.json"),
    )
    server_list = server_data.get("servers", [])
    if not server_list:
        return None

    server_words = [
        f"{s['server_id']} - {s['server_name']}" for s in server_list
    ]

    completer = FuzzyWordCompleter(words=server_words)

    style = Style.from_dict(
        {
            "prompt": "bold #00ff00",
            "": "#00ff00",
            "completion-menu.completion": "bg:#001100 #00ff00",
            "completion-menu.completion.current": "bg:#00ff00 #000000 bold",
            "scrollbar.background": "bg:#003300",
            "scrollbar.button": "bg:#00ff00",
        }
    )

    result = prompt(
        [("class:prompt", prompt_text)],
        completer=completer,
        complete_while_typing=True,
        style=style,
    ).strip()

    if not result:
        return None

    # Ambil server_id dari format "SRV001 - Alpha"
    return result.split(" - ")[0].strip()


def ask_for_ip() -> str:
    """Meminta input alamat IPv4 server dengan fitur autocomplete IP.

    Mengambil daftar server dari `FileHandler`, lalu menyediakan autocomplete
    berdasarkan alamat IP server tanpa metadata nama server.

    Input divalidasi menggunakan `IPv4Address`. Jika input bukan alamat IPv4
    yang valid, fungsi mengembalikan string kosong.

    Returns:
        str: Alamat IPv4 valid, atau string kosong jika tidak valid / tidak ada server.
    """
    server_list = FileHandler().load_server()
    if not server_list:
        return ""

    ip_words = [server.ip for server in server_list]

    completer = FuzzyWordCompleter(words=ip_words)

    style = Style.from_dict(
        {
            "prompt": "bold #00ff00",
            "": "#00ff00",
            "completion-menu.completion": "bg:#001100 #00ff00",
            "completion-menu.completion.current": "bg:#00ff00 #000000 bold",
            "scrollbar.background": "bg:#003300",
            "scrollbar.button": "bg:#00ff00",
        }
    )

    while True:
        ip_input = prompt(
            [("class:prompt", "Masukkan IP Server: ")],
            completer=completer,
            complete_while_typing=True,
            style=style,
        ).strip()

        try:
            ip_address = IPv4Address(ip_input)
            return str(ip_address)

        except AddressValueError:
            return ""
