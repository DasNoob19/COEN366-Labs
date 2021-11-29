import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = ('localhost', 11000)
print('Connecting to %s port %s' % server_address, file=sys.stderr)
sock.connect(server_address)

try:

    reicvFile = True
    message = input('Enter command ')
    print('Sending "%s"' % message)
    sock.sendall(message.encode())

    fileContent = ""

    while reicvFile:
        data = sock.recv(256)
        reicvMessage = data.decode()

        seperateMessage = reicvMessage.split(" - ")

        if seperateMessage[0] == "FILE-END":
            reicvFile = False

        fileContent = fileContent + seperateMessage[1]

        print(reicvMessage, file=sys.stderr)

    f = open("test.txt", "w")
    f.write(fileContent)
    f.close()

finally:
    print('Closing Socket', file=sys.stderr)
    sock.close()
