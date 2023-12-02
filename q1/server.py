from socket import *
import threading


def handle_client(client_socket, addr):

    username = client_socket.recv(1024).decode()
    print("client ", username," connected with ", addr," address")

    clients.append((username, client_socket))

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            msg = data.decode()

            if msg == "users":
                print('just udp request is accepted for getting users!')
            else:
                receiver, content = msg.split(';')
                if receiver == "all":
                    for client in clients:
                        if client[0] == username:
                            continue
                        client[1].send(("group -> " + username + ": " + content).encode())
                        print("group -> " + username + ": " + content)
                else:
                    for client in clients:
                        print(client)
                        if client[0] == receiver:
                            client[1].send(("pv -> " + username + ": " + content).encode())
                            print("pv -> " + username + ": " + content)
                            break


        except Exception as e:
            print("Error: ",e)
            break

    clients.remove((username, client_socket))
    print(username," disconnected")
    client_socket.close()

def handle_udp_users_request():
    while True:
        try:
            data, udp_address = udp_server_socket.recvfrom(1024)

            if not data:
                break

            msg = data.decode()
            print('UDP - message received:', msg)

            result = ""
            for client in clients:
                result += client[0] + "\n"
            print(result)

            udp_server_socket.sendto(result[:-1].encode(), udp_address)

        except Exception as e:
            print('error:', e)
            break

    print('disconnected')
    udp_server_socket.close()

if __name__ == '__main__':
    clients = []
    server_port = 13_000

    server_socket = socket(AF_INET, SOCK_STREAM)
    udp_server_socket = socket(AF_INET, SOCK_DGRAM)

    server_socket.bind(("", server_port))
    server_socket.listen(5)

    udp_server_socket.bind(('', server_port))

    print("server ready to receive...")

    users_udp_thread = threading.Thread(target=handle_udp_users_request)
    users_udp_thread.start()

    while 1:
        connection_socket, addr = server_socket.accept()
        print("new connection was accepted")
        client_thread = threading.Thread(target=handle_client, args=(connection_socket, addr))
        client_thread.start()
