server_list = []

class Server:
    def __init__(self, nama, ip, status, traffic):
        self.nama = nama
        self.ip = ip
        self.status = status
        self.traffic = traffic