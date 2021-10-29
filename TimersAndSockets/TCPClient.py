import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 11000)
print('Connecting to %s port %s' % server_address, file=sys.stderr)
sock.connect(server_address)

try:
    message = 'Ping'
    print('Sending "%s"' % message)
    sock.sendall(message.encode())

    amount_received = 0
    amount_expected = 1000

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('Received "%s"' % data, file=sys.stderr)

finally:
    print('Closing Socket', file=sys.stderr)
    sock.close()