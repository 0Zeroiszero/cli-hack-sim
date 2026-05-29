import os
import subprocess
import time
from colorama import Fore, Style, init


init(autoreset=True)


class CircularServerNode:
    # TODO: Menyesuaikan atribut pada 'src\data\server_status.json'
    def __init__(self, server_id, server_name, ip, status, vulnerable=False):
        self.server_id = server_id
        self.server_name = server_name
        self.ip = ip
        self.status = status
        self.previous_status = status
        self.vulnerable = vulnerable
        self.next = None


class CircularServerMonitor:
    def __init__(self):
        self.tail = None
        self.current = None

    def is_empty(self):
        return self.tail is None

    def add_server(self, server_id, server_name, ip, status, vulnerable=False):
        new_node = CircularServerNode(
            server_id=server_id,
            server_name=server_name,
            ip=ip,
            status=status,
            vulnerable=vulnerable,
        )

        if self.is_empty():
            self.tail = new_node
            self.tail.next = new_node
            self.current = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
            self.tail = new_node

    def move_next(self):
        if self.current is not None:
            self.current = self.current.next

    def red_text(self, text):
        return Fore.RED + Style.BRIGHT + str(text) + Style.RESET_ALL

    def green_text(self, text):
        return Fore.GREEN + Style.BRIGHT + str(text) + Style.RESET_ALL

    def yellow_text(self, text):
        return Fore.YELLOW + Style.BRIGHT + str(text) + Style.RESET_ALL

    def clear_screen(self):
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

    def check_current_server(self):
        if self.current is None:
            print("Belum ada server untuk dimonitor.")
            return

        changed = self.current.previous_status != self.current.status

        if changed:
            self.current.vulnerable = True
            self.current.previous_status = self.current.status

        self.clear_screen()

        color = self.red_text if self.current.vulnerable else self.green_text

        # TODO: Sesuaikan tampilan informasi server yang ingin ditampilkan
        print("+=======================================================+")
        print("|             CIRCULAR LINKED LIST MONITOR              |")
        print("+=======================================================+")
        print(color(f" Server ID       : {self.current.server_id}"))
        print(color(f" Server Name     : {self.current.server_name}"))
        print(color(f" IP Address      : {self.current.ip}"))
        print(color(f" Current Status  : {self.current.status}"))
        print(color(f" Previous Status : {self.current.previous_status}"))
        print(color(f" Vulnerable      : {self.current.vulnerable}"))
        print("+=======================================================+")

        if changed:
            print(
                self.red_text(
                    " CHANGE DETECTED : Status berubah dari histori sebelumnya"
                )
            )
            print(self.red_text(" ACTION          : vulnerable otomatis menjadi True"))
        else:
            print(self.yellow_text(" CHANGE DETECTED : Tidak ada perubahan"))

        if self.current.vulnerable:
            print(self.red_text(" ALERT           : SERVER VULNERABLE"))
        else:
            print(self.green_text(" ALERT           : SERVER AMAN"))

        print("+=======================================================+")
        print("Circular Route: server sekarang akan berpindah ke node berikutnya.")

    def update_status_demo(self, server_id, new_status):
        if self.is_empty():
            return False

        start = self.tail.next
        current = start

        while True:
            if current.server_id == server_id:
                current.status = new_status
                return True

            current = current.next

            if current == start:
                break

        return False

    def show_route(self):
        if self.is_empty():
            print("Circular linked list kosong.")
            return

        start = self.tail.next
        current = start
        route = []

        while True:
            route.append(current.server_id)
            current = current.next

            if current == start:
                break

        route.append(start.server_id)
        print(" -> ".join(route))

    def run_auto_monitor(self, delay=2):
        try:
            while True:
                self.check_current_server()
                self.move_next()
                time.sleep(delay)
        except KeyboardInterrupt:
            print("\nMonitoring dihentikan.")
