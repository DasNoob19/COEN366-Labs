import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 11000)
print('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)

sock.listen(1)

while True:
    print('Waiting for a connection', file=sys.stderr)
    connection, client_address = sock.accept()

    try:
        print('Connection From: ' + str(client_address), file=sys.stderr)

        while True:
            data = connection.recv(16)
            print('Received "%s"' % data, file=sys.stderr)

            if data:
                print('Sending data back to the client', file=sys.stderr)
                connection.sendall(data)
            else:
                print('No more data from ' + str(client_address), file=sys.stderr)
                break

    finally:
        connection.close()
