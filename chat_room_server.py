from socket import socket, gethostbyname, gethostname, SOCK_DGRAM, AF_INET
from threading import Thread
from queue import Queue

HOST = gethostbyname(gethostname())
PORT = 5000
ADDRESS = (HOST, PORT)
BUFFSIZE = 4096
s = socket(AF_INET, SOCK_DGRAM)
s.bind(ADDRESS)


def recvieve_msg(msg_socket, recv_msg):
    while True:
        msg, user = msg_socket.recvfrom(BUFFSIZE)
        recv_msg.put((msg, user))


def start_server():
    print('Host IP: '+str(HOST))
    clients = set()
    recv_msg = Queue()

    print('Server Running...')

    Thread(target=recvieve_msg, args=(s, recv_msg)).start()

    while True:
        while not recv_msg.empty():
            msg, user = recv_msg.get()
            if user not in clients:
                clients.add(user)
                continue
            clients.add(user)
            msg = msg.decode('utf-8')
            for client in clients:
                if client != user:
                    s.sendto(msg.encode('utf-8'), client)
            if msg.endswith('leave'):
                clients.remove(user)
                continue
            print(str(user)+msg)
    s.close()


if __name__ == '__main__':
    start_server()
