import asyncio
import datetime
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.prompt import Prompt  # Menggunakan Rich Prompt bawaan

console = Console()


def build_header(menu: str, sub_menu: str) -> Group:
<<<<<<< HEAD
    """Membangun header panel untuk tampilan menu.

    Args:
        menu: Nama menu utama (misal "Main Menu").
        sub_menu: Nama sub-menu saat ini (misal "Beranda").

    Returns:
        Group Rich berisi header panel, informasi waktu, dan rule.
    """
=======
>>>>>>> main
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = Panel(
        Text("HACKER NETWORK SIMULATION", justify="center", style="white"),
        border_style="green",
        title=f"{menu.upper()} - {sub_menu.upper()}",
        title_align="center",
    )
    info = Text()
    info.append(f"Menu Saat ini : {sub_menu}\n", style="bold green")
    info.append(f"Waktu         : {waktu}\n", style="bold green")
    return Group(header, "\n", info, "\n", Rule(style="white", characters="="))


async def main() -> None:
<<<<<<< HEAD
    """Menjalankan demo header menu dengan live refresh jam.

    Menampilkan header yang diperbarui setiap detik menggunakan Rich Live,
    sambil menunggu input pengguna melalui Rich Prompt di executor terpisah.
    """
=======
>>>>>>> main
    console.clear()

    # Membuat render live untuk tampilan atas
    with Live(
<<<<<<< HEAD
        build_header("Main Menu", "Beranda"),
        console=console,
        auto_refresh=False,
    ) as live:
        # Jalankan background task untuk terus mengupdate jam di header
        async def urus_header() -> None:
            """Memperbarui tampilan header setiap detik di background."""
=======
        build_header("Main Menu", "Beranda"), console=console, auto_refresh=False
    ) as live:
        # Jalankan background task untuk terus mengupdate jam di header
        async def urus_header():
>>>>>>> main
            while True:
                live.update(build_header("Main Menu", "Beranda"), refresh=True)
                await asyncio.sleep(1)

        header_task = asyncio.create_task(urus_header())

        # Karena Rich Prompt bawaan memblokir thread (sinkronus),
        # kita jalankan di dalam loop run_in_executor agar async task `urus_header` tetap jalan di background!
        loop = asyncio.get_running_loop()
        pilihan = await loop.run_in_executor(
            None,
            lambda: Prompt.ask(
                "\n[bold yellow]Pilih Menu (1-4, 0 untuk Keluar)[/]",
                choices=["1", "2", "3", "4", "0"],
                default="0",
            ),
        )

        # Hentikan update header setelah user memilih
        header_task.cancel()

    console.print(f"\n[bold green]Pilihan kamu:[/] {pilihan}")


if __name__ == "__main__":
    asyncio.run(main())
