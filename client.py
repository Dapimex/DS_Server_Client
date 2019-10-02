import socket
import sys
import os.path


def main():
    print(sys.argv)
    port = int(sys.argv[3])  # Reserve a port for your service every new transfer wants a new port or you must wait.
    sock = socket.socket()  # Create a socket object
    host = str(sys.argv[2])  # Get local machine name
    sock.connect((host, port))
    filename = str(sys.argv[1])
    sock.send(filename.encode())
    f = open(str(sys.argv[1]), 'rb')
    size = os.path.getsize(sys.argv[1])
    bytes_transported = 1024
    byte = f.read(1024)
    print(sock.recv(1024).decode())
    while byte:
        percent = bytes_transported * 100 // size
        print(f'{percent}%')
        bytes_transported += 1024
        sock.send(byte)
        byte = f.read(1024)
    f.close()
    print('End')
    sock.close()


if __name__ == "__main__":
    main()
