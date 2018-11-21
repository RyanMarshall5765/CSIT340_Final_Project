from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from threading import Thread
from random import randint
import sys
import os

HOST = gethostbyname(gethostname())
PORT = randint(5001, 10000)
ADDRESS = (HOST, PORT)
BUFFSIZE = 4096
s = socket(AF_INET, SOCK_DGRAM)
s.bind(ADDRESS)


def receive_msg(msg_socket):
    while True:
        try:
            msg, user = msg_socket.recvfrom(BUFFSIZE)
            print(msg.decode('utf-8'))
        except:
            pass


def start_client(host_ip):
    print('Client IP: '+str(HOST)+' Port: '+str(PORT))
    server_address = (str(host_ip), 5000)
    user_name = input('Please write your username here: ')
    if user_name == '':
        user_name = 'Guest'+str(randint(1, 100000))
        print('Your username is:'+user_name)
    s.sendto(user_name.encode('utf-8'), server_address)
    Thread(target=receive_msg, args=(s,)).start()
    while True:
        msg = input()
        if msg == 'leave':
            break
        elif msg == '':
            continue
        msg = '['+user_name+']' + ': ' + msg
        s.sendto(msg.encode('utf-8'), server_address)
    s.sendto(msg.encode('utf-8'), server_address)
    s.close()
    os._exit(1)


if __name__ == '__main__':
    start_client(sys.argv[1])
