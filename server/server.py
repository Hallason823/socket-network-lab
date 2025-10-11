import socket
import threading

class Server:
    def __init__(self, port, ip, header, selected_format, disconnect_message):
        self.port = port
        self.ip = ip
        self.header = header
        self.selected_format = selected_format
        self.disconnect_message = disconnect_message
        self.active_clients = []
        self.create_and_bind_socket()
        self.start_socket()

    def create_and_bind_socket(self):
        self.addr = (self.ip, self.port)
        print("[CREATING] server tcp socket is creating...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.addr)

    def handle_client(self, conn, addr):
        connected = True
        print(f"[NEW CONNECTION] {addr} connected.")
        while connected:
            msg_length = int(conn.recv(self.header).decode(self.selected_format))
            msg = conn.recv(msg_length).decode(self.selected_format)
            if msg == self.disconnect_message:
                connected = False
            print(f"[{addr}] {msg}")
        conn.close()

    def start_socket(self):
        print("[STARTING] server is starting...")
        self.server_socket.listen()
        while True:
            conn, addr = self.server_socket.accept()
            thread = threading.thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")