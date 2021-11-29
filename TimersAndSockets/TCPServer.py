import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
texts = []

server_address = ('0.0.0.0', 11000)
print('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)

sock.listen(1)

while True:
    print('Waiting for a connection', file=sys.stderr)
    connection, client_address = sock.accept()

    try:
        print('Connection From: ' + str(client_address), file=sys.stderr)

        while True:
            data = connection.recv(256)
            print('Received "%s"' % data.decode(), file=sys.stderr)

            if data:

                if data.decode() == "DOWNLOAD":
                    with open("data.txt") as chunks:
                        while True:
                            part = chunks.read(200)
                            texts.append(part)
                            if not part:
                                break

                    texts.remove('')

                    for i in range(len(texts)):
                        if i != len(texts) - 1:
                            message = "FILE - " + texts[i]
                        else:
                            message = "FILE-END - " + texts[i]
                        connection.sendall(message.encode())

                    texts.clear()
                else:
                    message = "DOWNLOAD-ERROR"
                    connection.sendall(message.encode())

            else:
                print('No more data from ' + str(client_address), file=sys.stderr)
                break

    finally:
        connection.close()
