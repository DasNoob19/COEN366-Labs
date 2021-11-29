import socket
import multiprocessing
import sys
import time
import threading
import datetime
import random

print(socket.gethostbyname(
    socket.gethostname()))  # have tp be inside the directory of the program or else it will be masked

TCPport = input('Enter your TCP Port for File Sharing')
UDPport = input('Enter your UDP Port')


# waits for connection and with a tcp port, and transfer files if needed
def ConnectWithClient():
    requestNumber = random.randint(0, 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (socket.gethostbyname(socket.gethostname()), int(TCPport))  # 111
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
                currentTime = datetime.datetime.now()
                with open('clientlog.txt', 'a+') as logfile:
                    logfile.write(
                        str(currentTime) + ' DOWNLOAD RQ: ' + str(requestNumber) + ' file name: ' + str(data.decode()))
                    logfile.write('\n')
                logfile.close()

                with open(data.decode(), 'r+') as f:
                    data = f.read().rstrip()

                    connection.sendall(data.encode())

            except:

                data = 'DOWNLOAD-ERROR RQ: ' + str(requestNumber) + ' Reason: file dont exist'
                connection.sendall(data.encode())
                requestNumber = requestNumber + 1

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

    s.bind((client_host, int(UDPport)))

    serverConnection = True

    while 1:

        # options=pyautogui.confirm('Enter option Gfg', buttons =['choice a', 'choice b', 'choice c','choice d'])
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
            msg1 = ''
            while len(msg1) < 1:
                msg1 = input('Enter the TCP port of the person holding the file')
                if len(msg1) < 1:
                    print("No TCP Port has been entered. Please try again. ")
            tempTCP(msg1)

        else:
            try:
                s.sendto(msg.encode(), (server_ip, port))

                d = s.recvfrom(1024)
                reply = d[0]
                addr = d[1]

                if reply.decode() == 'Please enter your username':
                    msg = input('Enter unique username')

                    s.sendto(msg.encode(), (server_ip, port))
                    d = s.recvfrom(1024)
                    reply = d[0]
                    s.sendto(TCPport.encode(), (server_ip, port))

                if reply.decode()[0:3] not in ['THE', 'ent']:
                    currentTime = datetime.datetime.now()
                    with open('clientlog.txt', 'a+') as logfile:
                        logfile.write(str(currentTime) + ' : ' + str(reply))
                        logfile.write('\n')
                    logfile.close()
                print('Server reply: ' + reply.decode())

            except socket.error as msg:
                print('Error')


def tempTCP(destination):
    tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:

        host = input('host?')
        print(int(destination))
        server_address = (host, int(destination))
        tempsock.connect(server_address)
        alert = input("Enter name of the Text File")
        while len(alert) < 1:
            alert = input("you cant just enter nothing you dummy")
        tempsock.sendall(alert.encode())

        counter = 0
        string = ''

        while True:

            data = tempsock.recv(50)  # length

            if not data:
                break
            if data.decode()[0:14] == 'DOWNLOAD-ERROR':
                currentTime = datetime.datetime.now()
                with open('clientlog.txt', 'a+') as logfile:
                    logfile.write(str(currentTime) + data.decode())
                    logfile.write('\n')
                logfile.close()
            elif len(data) < 50:
                print('last chunk' + data.decode(), ' at index' + str(counter))
                string = string + data.decode()
                print('File downloaded')
                currentTime = datetime.datetime.now()
                with open('clientlog.txt', 'a+') as logfile:
                    logfile.write(str(currentTime) + ' DOWNLOADED :' + alert)
                    logfile.write('\n')
                logfile.close()
                stdout = sys.stdout

                try:
                    sys.stdout = open(alert, 'w')
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
