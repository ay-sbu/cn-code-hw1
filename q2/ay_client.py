from socket import *
import threading
import os

# ------------------------------------------------------- send & receive
def send_message(client_socket):
    print('')
    print('-- send message: msg\n'
          '-- for exit: e')
    print('')

    while True:
        try:
            command = input('input command: ')
            msg = ''
            match command:
                case 'msg':
                    msg = input('input message: ')
                case 'e':
                    os._exit(0)
                case _:
                    print('command not found!!')
                    continue

            client_socket.send(msg.encode())

        except Exception as e:
            print('error:',  e)
            break

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode()
            print('message received:', message)

        except Exception as e:
            print('error:', e)
            break

# ------------------------------------------------------- main
if __name__ == '__main__':
    server_name = '127.0.0.1'
    server_port = 13_000

    command = ''
    while True:
        command = input('input connection type (tcp/udp): ')
        if command == 'tcp' or command == 'udp':
            break
        else:
            print('command not found!!')

    client_socket = ''

    match command:
        case 'tcp':
            client_socket = socket(AF_INET, SOCK_STREAM)
        case 'udp':
            client_socket = socket(AF_INET, SOCK_DGRAM)

    client_socket.connect((server_name, server_port))
    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))

    send_thread.start()
    receive_thread.start()

    receive_thread.join()
    send_thread.join()
    client_socket.close()
