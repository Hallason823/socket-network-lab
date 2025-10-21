import socket
import threading

class Server:
    def __init__(self, port, ip, header, selected_format, who_command, disconnect_message):
        self.port = port
        self.ip = ip
        self.header = header
        self.selected_format = selected_format
        self.who_command = who_command
        self.disconnect_message = disconnect_message
        self.active_clients = {}
        self.lock = threading.Lock()
        self.create_and_bind_socket()
        self.start_socket()

    def create_and_bind_socket(self):
        self.addr = (self.ip, self.port)
        print("[CREATING] server tcp socket is creating...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.addr)

    def receive_message(self, conn):
        try:
            msg_length = conn.recv(self.header).decode(self.selected_format)
            if not msg_length:
                return None
            msg_length = int(msg_length)
            return conn.recv(msg_length).decode(self.selected_format)
        except:
            return None

    def send_message(self, conn, msg):
        msg = msg.encode(self.selected_format)
        msg_header = str(len(msg)).encode(self.selected_format)
        msg_header += b' ' * (self.header - len(msg_header))
        conn.send(msg_header + msg)
    
    def register_nickname(self, conn, addr):
        nickname = self.receive_message(conn)
        if nickname is None:
            conn.close()
            return None
        with self.lock:
            if nickname in self.active_clients:
                self.send_message(conn, "FAILED: nickname in used")
                conn.close()
                return None
            else:
                self.active_clients[nickname] = conn
                print(f"[NEW USER] {nickname} joined from {addr}")
                self.send_message(conn, f"User {nickname} joined")
                print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
                return nickname

    def send_active_users(self, conn):
        with self.lock:
            users = ", ".join(self.active_clients.keys())
        self.send_message(conn, f"Connected users: {users}")

    def process_direct_message(self, conn, nickname, msg):
        try:
            dest_nick, dm_msg = msg.split(" ", 1)
            dest_nick = dest_nick[1:]
        except ValueError:
            self.send_message(conn, "WARNING: DM format is not well defined.")
            return
        with self.lock:
            if dest_nick not in self.active_clients:
                self.send_message(conn, f"ERROR: user not found {dest_nick}")
                return
            dest_conn = self.active_clients[dest_nick]
            self.send_message(dest_conn, f"FROM {nickname} [dm]: {dm_msg}")
        print(f"[DM] From {nickname} to {dest_nick}: {dm_msg}")

    def broadcast_message(self, nickname, msg):
        with self.lock:
            for user, user_conn in self.active_clients.items():
                if user != nickname:
                    self.send_message(user_conn, f"FROM {nickname} [all]: {msg}")
    
    def client_loop(self, conn, nickname):
        connected = True
        while connected:
            msg = self.receive_message(conn)
            if msg is None or msg.upper() == self.disconnect_message:
                connected = False
                break
            elif msg.upper() == self.who_command:
                self.send_active_users(conn)
            elif msg.startswith("@"):
                self.process_direct_message(conn, nickname, msg)
            else:
                self.broadcast_message(nickname, msg)
            print(f"[{nickname}] {msg}")

    def disconnect_client(self, conn, nickname):
        with self.lock:
            if nickname in self.active_clients:
                del self.active_clients[nickname]
        conn.close()
        print(f"[DISCONNECTED] {nickname} disconnected.")
        print(f"[ACTIVE CONNECTIONS] {len(self.active_clients)}")

    def handle_client(self, conn, addr):
        nickname = self.register_nickname(conn, addr)
        if nickname is None:
            return
        self.client_loop(conn, nickname)
        self.disconnect_client(conn, nickname)

    def start_socket(self):
        print("[STARTING] server is starting...")
        self.server_socket.listen()
        while True:
            conn, addr = self.server_socket.accept()
            self.send_message(conn, "Send your nickname to register, please.")
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = Server(ip=socket.gethostbyname(socket.gethostname()),port=12345,header=64,selected_format="utf-8",who_command="!WHO",disconnect_message="!QUIT")
