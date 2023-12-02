from socket import *
import threading

# ----------------------------------------------------------- tcp
def send_message():
    print("-- send message to specific user: pv\n"
          "-- send message to all user: all\n"
          "-- get list of all user: users\n"
          "-- for exit: e")
    while True:
        try:
            command = input()
            msg = ""
            match command:
                case "users":
                    msg = command
                    udp_client_socket.send(msg.encode())
                case "pv":
                    rcv = input("write your receiver username: ")
                    msg_ = input("write your message: ")
                    msg = rcv + ";" + msg_
                    client_socket.send(msg.encode())
                case "all":
                    msg_ = input("write your massage: ")
                    msg = "all" + ";" + msg_
                    client_socket.send(msg.encode())
                case "e":
                    break
                case _:
                    continue

        except Exception as e:
            print('Error: ', e)
            break


def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            print(message)

        except Exception as e:
            print("Error: ",e)
            break

def udp_receive():
    while True:
        try:
            data = udp_client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            print(message)

        except Exception as e:
            print("Error: ",e)
            break

# ----------------------------------------------------------- main
if __name__ == '__main__':
    server_name = '127.0.0.1'
    server_port = 13_000

    client_socket = socket(AF_INET, SOCK_STREAM)
    udp_client_socket = socket(AF_INET, SOCK_DGRAM)

    client_socket.connect((server_name, server_port))
    udp_client_socket.connect((server_name, server_port))
    username = input('username: ')
    client_socket.send(username.encode())

    send_thread = threading.Thread(target=send_message)
    send_thread.start()

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    udp_receive_thread = threading.Thread(target=udp_receive)
    udp_receive_thread.start()

    udp_receive_thread.join()
    receive_thread.join()
    send_thread.join()
    client_socket.close()
