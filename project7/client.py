import socket
import sys
import threading
import datetime
import random
import logging

logging.basicConfig(filename='client_log.txt')

print(socket.gethostbyname(socket.gethostname()))  # have tp be inside the directory of the program or else it will be masked

tcp_port = input('Enter your TCP Port for File Sharing')
udp_port = input('Enter your UDP Port') #Prevent Similar UDP


# waits for connection and with a tcp port, and transfer files if needed
def ConnectWithClient():
    request_number = random.randint(0, 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (socket.gethostbyname(socket.gethostname()), int(tcp_port))  # 111
    print('Starting up on %s port %s' % server_address)
    sock.bind(server_address)

    sock.listen(1)

    while True:
        print('Waiting for a connection')
        connection, client_address = sock.accept()

        try:
            print('Connection From: ' + str(client_address))
            data = connection.recv(200)

            try:
                logging.info('DOWNLOAD RQ: ' + str(request_number) + ' file name: ' + str(data.decode()))

                with open(data.decode(), 'r+') as f:
                    data = f.read().rstrip()
                    connection.sendall(data.encode())
            except:
                data = 'DOWNLOAD-ERROR RQ: ' + str(request_number) + ' Reason: file doesnt exist'
                connection.sendall(data.encode())

        except socket.error as msg:
            print('Error')
        finally:
            connection.close()


def ConnectWithServer():
    client_host = '0.0.0.0'

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    s.bind((client_host, int(udp_port)))

    serverConnection = True

    while 1:
        # Trying to connect to master server
        while serverConnection:
            server_address = ''
            while ":" not in server_address:
                server_address = input('Enter the server address of the UDP (Format: \'IP address\':\'UDP Port\')')
                if ":" not in server_address:
                    print('ERROR - The address must in the format \'IP address\':\'UDP Port\'')

            server_ip = server_address.split(":")[0]
            port = int(server_address.split(":")[1])
            print('Connecting to server ' + server_ip)
            msg = 'Sending Connection'
            try:
                s.sendto(msg.encode(), (server_ip, port))
                d = s.recvfrom(1024)
                reply = d[0]
                addr = d[1]
                if reply.decode() == 'Connected':
                    print('Connected to ' + server_ip)
                    serverConnection = False
            except socket.error as msg:
                print('Connection Failed: Please try again')

        msg = input('Enter message to send')

        if not msg:
            msg = ''
        if msg == "DOWNLOAD":
            filename = input('Enter the filename to download')
            clientAddress = input('Enter the address of the client holding the file')
            msg = msg + ' - ' + filename + ' - ' + clientAddress

            try:
                s.sendto(msg.encode(), (server_ip, port))
                d = s.recvfrom(1024)
                reply = d[0].decode()

                if reply == "DOWNLOAD":
                    tempTCP(clientAddress, filename)
                else:
                    print(reply)

            except socket.error as msg:
                print('Error')


        elif msg == "REGISTER":
            username = input('Please enter your username')
            msg = msg + " - " + username + " - " + tcp_port
            try:
                s.sendto(msg.encode(),(server_ip, port))
                d = s.recvfrom(1024)
                reply = d[0]
                print('Server reply: ' + reply.decode())

            except socket.error as msg:
                print('Error')

        elif msg == "PUBLISH":
            file = input('Please enter the name of the file that you wish to publish (\'FILENAME\'.txt)')
            msg = msg + " - " + file

            try:
                s.sendto(msg.encode(), (server_ip, port))
                d = s.recvfrom(1024)
                reply = d[0]
                print('Server reply: ' + reply.decode())

            except socket.error as msg:
                print('Error')

        elif msg == "REMOVE":
            filename = input('Enter the name of the file to remove (\'FILENAME\'.txt)')
            msg = msg + ' - ' + filename
            try:
                s.sendto(msg.encode(), (server_ip, port))
                d = s.recvfrom(1024)
                reply = d[0]
                print('Server reply: ' + reply.decode())

            except socket.error as msg:
                print('Error')

        else:
            try:
                s.sendto(msg.encode(), (server_ip, port))

                d = s.recvfrom(1024)
                reply = d[0]

                if reply.decode()[0:3] not in ['THE', 'ent']:
                    logging.info(reply)
                print('Server reply: ' + reply.decode())

            except socket.error as msg:
                print('Error')


def tempTCP(targetDestination, filename):
    tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:

        destination = targetDestination.split(':')
        server_address = (destination[0], int(destination[1]))
        tempsock.connect(server_address)
        tempsock.sendall(filename.encode())

        counter = 0
        string = ''

        while True:

            data = tempsock.recv(200)  # length

            if not data:
                break
            if data.decode()[0:14] == 'DOWNLOAD-ERROR':
                logging.info(data.decode())
            elif len(data) < 200:
                print('last chunk' + data.decode(), ' at index' + str(counter))
                string = string + data.decode()
                print('File downloaded')
                logging.info(f'DOWNLOADED : {filename}')
                stdout = sys.stdout

                try:
                    sys.stdout = open(filename, 'w')
                    print(string)

                finally:
                    sys.stdout.close()  # close file.txt
                    sys.stdout = stdout

                break
            else:
                print('Received ' + data.decode(), ' at index' + str(counter))
                counter = counter + len(data)
                string = string + data.decode()
    except:
        print('Wrong port, make sure you enter the right port number ')
        tempsock.close()
    finally:
        tempsock.close()

    # creating multiple processes


proc1 = threading.Thread(target=ConnectWithServer)
proc2 = threading.Thread(target=ConnectWithClient)

# Initiating process 1

proc1.start()

# Initiating process 2

proc2.start()

# Waiting until proc1 finishes

proc1.join()

# Waiting until proc2 finishes

proc2.join()
