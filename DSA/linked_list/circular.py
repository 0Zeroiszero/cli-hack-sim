"""
@author: Abdullah Affandi
"""

import os
import subprocess
import time

from src.server import Server
from utils.text_color_changer import red_text, green_text, yellow_text


class CircularServerNode(Server):
    def __init__(
        self,
        *,
        server_id: str,
        server_name: str,
        ip: str,
        status: str,
        vulnerable: bool = False,
        access: str = "LOCKED",
    ):
        super().__init__(nama=server_name, id=server_id, ip=ip, status=status)

        # Atribut tambahan khusus circular linked list
        self.vulnerable = vulnerable
        self.access = access
        self.previous_status = status
        self.next = None


class CircularServerMonitoring:
    def __init__(self):
        self.tail = None
        self.current = None

    def is_empty(self):
        return self.tail is None

    def add_server(
        self, *, server_id, server_name, ip, status, vulnerable=False, access="LOCKED"
    ):
        new_node = CircularServerNode(
            server_id=server_id,
            server_name=server_name,
            ip=ip,
            status=status,
            vulnerable=vulnerable,
            access=access,
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

        color = red_text if self.current.vulnerable else green_text

        print("+=======================================================+")
        print("|             CIRCULAR LINKED LIST MONITOR              |")
        print("+=======================================================+")
        print(color(f" Server ID       : {self.current.id}"))
        print(color(f" Server Name     : {self.current.nama}"))
        print(color(f" IP Address      : {self.current.ip}"))
        print(color(f" Current Status  : {self.current.status}"))
        print(color(f" Previous Status : {self.current.previous_status}"))
        print(color(f" Access          : {self.current.access}"))
        print(color(f" Vulnerable      : {self.current.vulnerable}"))
        print("+=======================================================+")

        if changed:
            print(red_text(" CHANGE DETECTED : Status berubah dari histori sebelumnya"))
            print(red_text(" ACTION          : vulnerable otomatis menjadi True"))
        else:
            print(yellow_text(" CHANGE DETECTED : Tidak ada perubahan"))

        if self.current.vulnerable:
            print(red_text(" ALERT           : SERVER VULNERABLE"))
        else:
            print(green_text(" ALERT           : SERVER AMAN"))

        
    def update_status_demo(self, server_id, new_status):
        if self.is_empty():
            return False

        start = self.tail.next
        current = start

        while True:
            if current.id == server_id:
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
            route.append(current.id)
            current = current.next

            if current == start:
                break

        route.append(start.id)
        print(" -> ".join(route))

    def run_auto_monitor(self, delay=2):
        try:
            while True:
                self.check_current_server()
                self.move_next()
                time.sleep(delay)
        except KeyboardInterrupt:
            print("\nMonitoring dihentikan.")
