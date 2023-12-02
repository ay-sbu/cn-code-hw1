from socket import *
import threading
from collections import Counter

# ---------------------------------------------------- utils
def convert_chr_to_num(inputchr):
    inputchr = inputchr.lower()
    return (ord(inputchr) - ord('a')) // 2

def tcp_util(inputstr):
    res = Counter(inputstr)
    res = min(res, key = res.get)

    outstr = ''
    for i in inputstr:
        if i == ' ':
            outstr += ' '
        else:
            outstr += str(convert_chr_to_num(i))

    outstr += ', '
    outstr += str(convert_chr_to_num(res))

    return outstr

def udp_util(inputstr):
    res = Counter(inputstr)
    res = max(res, key = res.get)

    return inputstr.upper()[::-1] + ', ' + res.upper()

# ---------------------------------------------------- tcp
def handle_tcp_client(client_socket, addr):
    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                break

            msg = data.decode()
            print('TCP - message received:', msg)

            if msg == 'exit server':
                break

            msg = tcp_util(msg)

            client_socket.send(msg.encode())

        except Exception as e:
            print('error:', e)
            break

    print('disconnected')
    client_socket.close()

def handler_tcp_thread(server_socket):
    while True:
        connection_socket, addr = server_socket.accept()

        print('new TCP connection was accepted')

        client_thread = threading.Thread(target=handle_tcp_client, args=(connection_socket, addr))
        client_thread.start()

# ---------------------------------------------------- udp
def handle_udp_client(client_socket):
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)

            if not data:
                break

            msg = data.decode()
            print('UDP - message received:', msg)

            if msg == 'exit server':
                break

            msg = udp_util(msg)

            client_socket.sendto(msg.encode(), addr)

        except Exception as e:
            print('error:', e)
            break

    print('disconnected')
    client_socket.close()

# ---------------------------------------------------- main
if __name__ == '__main__':
    server_name = '127.0.0.1'
    server_port = 13_000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind((server_name, server_port))
    tcp_socket.listen(5)

    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind((server_name, server_port))

    print('server ready to receive...')

    tcp_handler = threading.Thread(target=handler_tcp_thread, args=(tcp_socket, ))
    tcp_handler.start()

    client_thread = threading.Thread(target=handle_udp_client, args=(udp_socket, ))
    client_thread.start()
