import socket
from threading import Thread
import os.path


current_connections = []


class ClientListener(Thread):
    def __init__(self, name, soc: socket.socket):
        super().__init__(daemon=True)
        self.name = name
        self.socket = soc

    def _close(self):
        current_connections.remove(self.socket)
        self.socket.close()
        print(self.name + ' disconnected')

    def run(self):
        file_base = self.socket.recv(1024).decode()
        if os.path.isfile(file_base):
            copy_index = 1
            file = file_base + "_copy_" + str(copy_index)
            while os.path.isfile(file):
                copy_index += 1
                file = "copy_{}_{}".format(copy_index, file_base)
        else:
            file = file_base
        f = open(file, "wb")
        msg = "File {} is created".format(f)
        self.socket.send(msg.encode())
        while True:
            data = self.socket.recv(1024)
            if data:
                f.write(data)
            else:
                self._close()
                return


def main():
    connection_pointer = 1
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind(('', 8800))
    soc.listen()
    print("Listen...")
    while True:
        connection, address = soc.accept()
        current_connections.append(connection)
        name = 'u' + str(connection_pointer)
        connection_pointer += 1
        print(str(address) + ' connected as ' + name)
        ClientListener(name, connection).start()


if __name__ == "__main__":
    main()
