"""
@author: Abdullah Affandi
"""

from tabulate import tabulate

import subprocess
import os

from src.server import Server
from utils.text_color_changer import (
    selected_text,
    side_text,
    green_text,
    red_text,
    yellow_text,
)


class ServerNode(Server):
    def __init__(self, *, server_id: str, server_name: str, ip: str, status: str):
        super().__init__(nama=server_name, id=server_id, ip=ip, status=status)

        self.prev = None
        self.next = None


class ServerCarousel:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_server(self, *, server_id: str, server_name: str, ip: str, status: str):
        new_node = ServerNode(
            server_id=server_id, server_name=server_name, ip=ip, status=status
        )

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def move_up(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        else:
            print(yellow_text("Sudah berada di server paling atas."))
            input("Tekan Enter untuk lanjut...")

    def move_down(self):
        if self.current and self.current.next:
            self.current = self.current.next
        else:
            print(yellow_text("Sudah berada di server paling bawah."))
            input("Tekan Enter untuk lanjut...")

    def clear_screen(self):
        command = "cls" if os.name == "nt" else "clear"
        subprocess.run(command, shell=True)

    def display_carousel(self) -> None:
        if self.current is None:
            print("Data server kosong.")
            return

        rows = []

        if self.current.prev:
            rows.append(
                [
                    side_text("PREVIOUS"),
                    side_text(self.current.prev.id),
                    side_text(self.current.prev.nama),
                    side_text(self.current.prev.ip),
                    side_text(self.current.prev.status),
                ]
            )

        rows.append(
            [
                selected_text("SELECTED"),
                selected_text(self.current.id),
                selected_text(self.current.nama),
                selected_text(self.current.ip),
                selected_text(self.current.status),
            ]
        )

        if self.current.next:
            rows.append(
                [
                    side_text("NEXT"),
                    side_text(self.current.next.id),
                    side_text(self.current.next.nama),
                    side_text(self.current.next.ip),
                    side_text(self.current.next.status),
                ]
            )

        print(
            tabulate(
                rows,
                headers=[
                    "Position",
                    "Server ID",
                    "Server Name",
                    "IP Address",
                    "Status",
                ],
                tablefmt="plain",
            )
        )

    def show_current_detail(self) -> None:
        if self.current is None:
            print("Tidak ada server yang dipilih.")
            return

        title = "DETAIL SERVER YANG DIPILIH"
        width = 55

        print()
        print(green_text("+" + "=" * width + "+"))
        print(green_text("|" + title.center(width) + "|"))
        print(green_text("+" + "=" * width + "+"))

        rows = [
            ["Server ID", ":", self.current.id],
            ["Server Name", ":", self.current.nama],
            ["IP Address", ":", self.current.ip],
            ["Status", ":", self.current.status],
        ]

        print(green_text(tabulate(rows, tablefmt="plain")))

    def run(self):
        while True:
            self.clear_screen()

            print("+=======================================================+")
            print("|                    DAFTAR SERVER                      |")
            print("+=======================================================+")
            print()

            self.display_carousel()
            self.show_current_detail()

            print("\n[W] Naik ke server sebelumnya")
            print("[S] Turun ke server berikutnya")
            print("[Q] Keluar")

            choice = input("\nPilih: ").lower()

            if choice == "w":
                self.move_up()
            elif choice == "s":
                self.move_down()
            elif choice == "q":
                break
            else:
                print(red_text("Pilihan tidak valid."))
                input("Tekan Enter untuk lanjut...")
