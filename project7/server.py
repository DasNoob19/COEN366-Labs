import socket
import sys
import json
import threading
from queue import Queue
import random
import logging

logging.basicConfig(filename='logs.txt')

HOST = '0.0.0.0'
PORT = 3000
print('Initializing server at port the default UDP PORT: ', PORT)
print('IP ADDRESS: ', socket.gethostbyname(socket.gethostname()))

requestNumber = random.randint(0, 40_000)
# check if client_list exists, if not create one with empty dictionary inside

work_queue: Queue = Queue()


def send_message_to_client_address(msg: str, client_address: str):
    encoded_msg = msg.encode()
    print("Sending to " + str(client_address) + ": " + msg)
    server_socket.sendto(encoded_msg, client_address)


def get_client_list():
    with open('client_list.json', 'r+') as reader:
        client_list_checker = json.load(reader)
    return client_list_checker


def save_client_list(client_list_object):
    with open('client_list.json', 'w') as writer:
        writer.write(json.dumps(client_list_object))


def is_this_a_client(client_address):
    client_list_checker = get_client_list()
    for key, values in client_list_checker.items():
        if str(client_address[0]) == values[0]:
            return True
    else:
        return False


def do_actions(data, client_address, request_number):

    print('Command Received from ' + str(client_address) + ": " +
          data.decode())

    if not data:
        pass

    is_client = False
    clientMessage = data.decode()
    action = clientMessage.split()[0]

    client_list_checker = get_client_list()
    if client_list_checker:
        is_client = is_this_a_client(client_address)

    if clientMessage == 'Sending Connection':

        send_message_to_client_address('Connected', client_address)

    elif action == 'REGISTER':
        messageSplit = clientMessage.split(' - ')
        name = messageSplit[1]
        client_list_object = get_client_list()
        yida = client_list_object

        if name in client_list_object:
            message = f'REGISTER-DENIED RQ: {request_number}. Reason: {name} already exists'
            send_message_to_client_address(message,
                                           client_address=client_address)
            logging.info(message)
        else:
            yida.setdefault(name, [client_address[0], str(client_address[1])])

            message = 'REGISTERED ' + str(request_number)
            send_message_to_client_address(msg=message,
                                           client_address=client_address)

            tcp_port = messageSplit[2]
            yida[name].append(tcp_port)
            yida[name].append([])

            save_client_list(yida)

            logging.info(f'REGISTERED RQ: {request_number}: {name}')

    elif action == 'SECRET' and is_client:

        tempZinedine(client_address[0], 69)
    elif action == 'SECRET1' and is_client:

        tempZinedine1(client_address[0], 69)

    elif action == 'DE-REGISTER' and is_client:
        client_list_object = get_client_list()

        for key, values in client_list_object.items():
            if str(client_address[0]) == values[0]:
                client_list_object.pop(key)
                logging.info(f'DE-REGISTER RQ: {request_number} Name: {key}')
                message = 'DE-REGISTER RQ: ' + str(
                    request_number) + ' Name: ' + key
                send_message_to_client_address(msg=message,
                                               client_address=client_address)
                break

        save_client_list(client_list_object)

    elif action == 'PUBLISH' and is_client:
        client_list_object = get_client_list()
        publish_checker = False
        publishMessage = clientMessage.split(' - ')

        for key, values in client_list_object.items():
            if str(client_address[0]) == values[0]:
                filename = publishMessage[1]
                values[3].append(filename)
                logging.info(
                    f'PUBLISH RQ : {request_number} Name : {key} file : {filename}'
                )

                message = f' PUBLISH RQ : {request_number}'
                send_message_to_client_address(msg=message,
                                               client_address=client_address)

                publish_checker = True
                break

        if not publish_checker:
            message = ' PUBLISH-DENIED RQ : ' + str(request_number)
            send_message_to_client_address(message, client_address)

        save_client_list(client_list_object)

    elif action == 'REMOVE' and is_client:
        client_list_object = get_client_list()
        removeFile = clientMessage.split(' - ')
        remove_checker = False

        for key, values in client_list_object.items():
            if str(client_address[0]) == values[0]:
                filename = removeFile[1]
                for i in values[3]:
                    if i == filename:
                        values[3].remove(i)
                        logging.info(
                            f'REMOVE RQ : {request_number} Name : {key} File to removed : {filename}'
                        )
                        message = 'REMOVE RQ : ' + str(request_number)
                        send_message_to_client_address(message, client_address)
                        request_number = request_number + 1
                        remove_checker = True
                        break

        if not remove_checker:
            message = 'REMOVE-DENIED RQ : ' + str(
                request_number) + ' REASON : File dont exist'
            send_message_to_client_address(message, client_address)

        save_client_list(client_list_object)

    elif action == 'RETRIEVE-ALL' and is_client:
        client_list_object = get_client_list()

        logging.info('RETRIEVE-ALL RQ: ' + str(request_number))

        everyOneInfo = json.dumps(client_list_object)
        message = 'RETRIEVE RQ: ' + str(request_number) + ' ' + everyOneInfo
        send_message_to_client_address(message, client_address)

    elif action == 'RETRIEVE-INFOT' and is_client:
        client_list_object = get_client_list()

        retrieveMessage = clientMessage.split(' - ')
        name = retrieveMessage[1]

        name_checker = False
        for key, values in client_list_object.items():
            if key == name:
                message = 'RETRIEVE-INFOT RQ: ' + str(request_number) + ' Name: ' + key + ', IP: ' + values[0] + \
                          ', UDP port: ' + values[1] + ', TCP Port: ' + values[2] + ', List of files available: '
                for i in values[3]:
                    message += i
                    message += ', '

                send_message_to_client_address(message, client_address)
                name_checker = True
                break

        if not name_checker:
            message = 'RETRIEVE-ERROR RQ: ' + str(
                request_number) + ' Reason : Person does not exist'
            send_message_to_client_address(message, client_address)

    elif action == 'SEARCH-FILE' and is_client:
        client_list_object = get_client_list()

        file_checker = False
        file_info = ''
        searchFileMessage = clientMessage.split(' - ')
        filename = searchFileMessage[1]

        logging.info(
            f'SEARCH-FILE RQ : {request_number} File-name : {filename}')

        for key, values in client_list_object.items():
            for i in values[3]:
                if i == filename:
                    file_info += 'Name: ' + key + ', IP: ' + values[
                        0] + ', TCP Port: ' + values[2] + '    '
                    file_checker = True

        if not file_checker:
            message = ' SEARCH-ERROR RQ : ' + str(
                request_number) + ' Reason : File does not exist'
            send_message_to_client_address(message, client_address)

        else:
            message = 'SEARCH-FILE RQ ' + str(request_number) + ' ' + file_info
            send_message_to_client_address(message, client_address)

    elif action == 'DOWNLOAD' and is_client:

        downloadMessage = clientMessage.split(' - ')
        filename = downloadMessage[1]
        TCP_Address = downloadMessage[2].split(':')
        client_list_object = get_client_list()
        file_checker = False
        for key, values in client_list_object.items():
            if values[0] == TCP_Address[0] and values[2] == TCP_Address[1]:
                for i in values[3]:
                    if i == filename:
                        file_checker = True

        if not file_checker:
            message = 'DOWNLOAD-ERROR RQ : ' + str(
                request_number) + ' Reason : File is not published'
            send_message_to_client_address(message, client_address)
        else:
            message = 'DOWNLOAD'
            send_message_to_client_address(message, client_address)

    elif action == 'UPDATE' and is_client:
        client_list_object = get_client_list()
        updateMessage = clientMessage.split(' - ')
        update_checker = False
        for key, values in client_list_object.items():

            if str(client_address[0]) == values[0]:
                logging.info(
                    f'UPDATE-CONTACT RQ: {request_number} Name: {key} IP: {values[0]} UDP: {values[1]} TCP: {values[2]}'
                )
                username = key  # temp value stored to be used in line 420
                new_ip = values[0]
                new_tcp = values[2]
                new_udp = values[1]

                if not updateMessage[1] == '':
                    values[0] = updateMessage[1]
                    new_ip = values[0]
                if not updateMessage[2] == '':
                    values[1] = updateMessage[2]
                    new_udp = values[1]
                if not updateMessage[3] == '':
                    values[2] = updateMessage[3]
                    new_tcp = values[2]
                update_checker = True

        save_client_list(client_list_object)

        if not update_checker:
            message = 'UPDATE DENIED RQ: ' + str(
                request_number) + ' Name: ' + username
            send_message_to_client_address(message, client_address)
        else:
            message = 'UPDATE CONFIRMED RQ: ' + str(
                request_number
            ) + ' Name: ' + username + ' IP: ' + new_ip + ' UDP: ' + new_udp + ' TCP:' + new_tcp

            logging.info(
                f'UPDATE CONFIRMED RQ: {request_number} Name: {username} IP: {new_ip} UDP: {new_udp} TCP: {new_tcp}'
            )
        send_message_to_client_address(message, client_address)

    elif not is_client:
        message = 'You are not a client. Please REGISTER before entering other commands'
        send_message_to_client_address(message, client_address)

    else:
        message = 'This request does not exist'
        send_message_to_client_address(message, client_address)


def taskRunner(data_received, request_number):
    data = data_received[0]
    client_address = data_received[1]

    logging.info('Received message from ' + str(client_address))
    work_queue.put((data, client_address, request_number))


def action_assigner():
    while True:
        if work_queue.qsize() != 0:
            data, client_address, request_number = work_queue.get()
            do_actions(data, client_address, request_number)


def tempZinedine(host, destination):
    tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_address = (host, int(destination))
        tempsock.connect(server_address)
        file = open('zidane.jpg', 'rb')
        image_data = file.read(2048)

        while image_data:
            tempsock.send(image_data)
            image_data = file.read(2048)
    except:
        print('Sorry you did not get the secret picture')
        tempsock.close()
    finally:
        tempsock.close()


def tempZinedine1(host, destination):
    tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_address = (host, int(destination))
        tempsock.connect(server_address)
        file = open('zizou.jpg', 'rb')
        image_data = file.read(2048)

        while image_data:
            tempsock.send(image_data)
            image_data = file.read(2048)
    except:
        print('Sorry you did not get the secret picture')
        tempsock.close()
    finally:
        tempsock.close()


def task_putter():
    request_number = 0
    while True:
        data_received = server_socket.recvfrom(1024)
        request_number += 1
        taskRunner(data_received, request_number)


try:
    print(get_client_list())
except FileNotFoundError:
    logging.info('Creating an empty clientlist')
    empty_client_list = {}
    save_client_list(empty_client_list)

# Initialize socket
try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logging.info('Sucessfully created socket')
except socket.error as msg:
    logging.info(
        f'Failed to created socket. Error code: {msg[0]} Message: {msg[1]}')
    sys.exit()

# Initialize bind
try:
    server_socket.bind((HOST, PORT))
    logging.info('Socket bind complete')
    print('Socket bind complete')
except socket.error as msg:
    print('Bind Failed. Error code: ' + str(msg[0]) + ' Message ' + msg[1])
    logging.info('Socket bind error')
    sys.exit()

# Keep receiving data
try:
    thread_task = threading.Thread(target=task_putter)
    action_thread = threading.Thread(target=action_assigner)

    action_thread.start()
    thread_task.start()

    action_thread.join()
    thread_task.join()

except Exception as e:
    server_socket.close()
