from socket import *


def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    port = 9000

    server_socket.bind(("0.0.0.0", port))
    print("Server listening on port {!s}".format(port))
    server_socket.listen(5)
    while True:
        (client, address) = server_socket.accept()
        print("Connection address: {!s}".format(address))

        client.close()


if __name__ == "__main__":
    main()
