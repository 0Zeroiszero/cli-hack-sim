from tabulate import tabulate
from colorama import Fore, Style, init
import os


init(autoreset=True)


class ServerNode:
    # TODO: Sesuaikan atribut server
    def __init__(self, server_id, server_name, ip, status):
        self.server_id = server_id
        self.server_name = server_name
        self.ip = ip
        self.status = status
        self.prev = None
        self.next = None


class ServerCarousel:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_server(self, server_id, server_name, ip, status):
        new_node = ServerNode(server_id, server_name, ip, status)

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
            print(Fore.YELLOW + "Sudah berada di server paling atas.")
            input("Tekan Enter untuk lanjut...")

    def move_down(self):
        if self.current and self.current.next:
            self.current = self.current.next
        else:
            print(Fore.YELLOW + "Sudah berada di server paling bawah.")
            input("Tekan Enter untuk lanjut...")

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def selected_text(self, text):
        return Fore.GREEN + Style.BRIGHT + str(text) + Style.RESET_ALL

    def side_text(self, text):
        return Fore.GREEN + Style.DIM + str(text) + Style.RESET_ALL

    def display_carousel(self):
        if self.current is None:
            print("Data server kosong.")
            return

        rows = []

        if self.current.prev:
            rows.append([
                self.side_text("PREVIOUS"),
                self.side_text(self.current.prev.server_id),
                self.side_text(self.current.prev.server_name),
                self.side_text(self.current.prev.ip),
                self.side_text(self.current.prev.status)
            ])

        rows.append([
            self.selected_text("SELECTED"),
            self.selected_text(self.current.server_id),
            self.selected_text(self.current.server_name),
            self.selected_text(self.current.ip),
            self.selected_text(self.current.status)
        ])

        if self.current.next:
            rows.append([
                self.side_text("NEXT"),
                self.side_text(self.current.next.server_id),
                self.side_text(self.current.next.server_name),
                self.side_text(self.current.next.ip),
                self.side_text(self.current.next.status)
            ])

        print(tabulate(
            rows,
            headers=["Position", "Server ID", "Server Name", "IP Address", "Status"],
            tablefmt="grid"
        ))

    def show_current_detail(self):
        if self.current is None:
            print("Tidak ada server yang dipilih.")
            return

        print("\n" + Fore.GREEN + Style.BRIGHT + "+=======================================================+")
        print(Fore.GREEN + Style.BRIGHT + "|                DETAIL SERVER YANG DIPILIH             |")
        print(Fore.GREEN + Style.BRIGHT + "+=======================================================+")
        print(Fore.GREEN + Style.BRIGHT + f" Server ID   : {self.current.server_id}")
        print(Fore.GREEN + Style.BRIGHT + f" Server Name : {self.current.server_name}")
        print(Fore.GREEN + Style.BRIGHT + f" IP Address  : {self.current.ip}")
        print(Fore.GREEN + Style.BRIGHT + f" Status      : {self.current.status}")
        print(Fore.GREEN + Style.BRIGHT + "+=======================================================+")

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
                print(Fore.RED + "Pilihan tidak valid.")
                input("Tekan Enter untuk lanjut...")