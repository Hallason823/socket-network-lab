import socket
import threading

class Client:
    def __init__(self, ip, port, header, selected_format, who_command, disconnect_message):
        self.ip = ip
        self.port = port
        self.header = header
        self.selected_format = selected_format
        self.who_command = who_command
        self.disconnect_message = disconnect_message

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))

    def send_message(self, msg):
        msg = msg.encode(self.selected_format)
        msg_header = str(len(msg)).encode(self.selected_format)
        msg_header += b' ' * (self.header - len(msg_header))
        self.client_socket.send(msg_header + msg)

    def receive_message(self):
        try:
            msg_header = self.client_socket.recv(self.header).decode(self.selected_format)
            if not msg_header:
                return None
            msg_length = int(msg_header.strip())
            return self.client_socket.recv(msg_length).decode(self.selected_format)
        except:
            return None

    def listen_for_messages(self):
        while True:
            try:
                msg = self.receive_message()
                if msg is None:
                    print("[SERVER DISCONNECTED]")
                    break
                print(msg)
            except Exception as e:
                print(f"[ERROR] {e}")
                break

    def start(self):
        self.connect()
        print(self.receive_message())
        nickname = input("Enter your nickname: ")
        self.send_message(nickname)
        thread = threading.Thread(target=self.listen_for_messages)
        thread.daemon = True
        thread.start()
        while True:
            msg = input("")
            if msg.upper() == self.disconnect_message.upper():
                self.send_message(self.disconnect_message)
                break
            elif msg.upper() == self.who_command.upper():
                self.send_message(self.who_command)
            else:
                self.send_message(msg)
        self.client_socket.close()

if __name__ == "__main__":
    client = Client(ip=socket.gethostbyname(socket.gethostname()), port=12345, header=64, selected_format="utf-8", disconnect_message="!QUIT", who_command="!WHO")
    client.start()