import socket
import sys

HOST = '0.0.0.0'
PORT = 8888

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except socket.error as msg:
    print('Failed to created socket. Error code :' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind Failed. Error code: ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print ('Socket bind complete')

while 1:
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]

    if not data:
        break

    message = 'OK...'
    reply = message.encode() + data

    s.sendto(reply,addr)
    print('Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + str(data.strip()))

s.close()