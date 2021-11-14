import json
import time
from typing import List, Tuple, Union
from dataclasses import dataclass
from queue import Queue
import socket
import threading

from utils.client_information import ClientInformation
from utils.action import Action, ActionTypes
from utils.message import Message


@dataclass
class RequestLog:
    request_number: int
    sent_from: str
    sent_to: str


class MasterServer:
    def __init__(self, host: str, port: int, buffer_size: int):
        self.logs: List[(RequestLog, str)]
        self.connected_clients: List[ClientInformation] = []
        self.action_queue: Queue[Tuple[str, Action]] = Queue()

        self._host: str = host
        self._port: int = port
        self._buffer_size: int = buffer_size

        self._sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self._sock.settimeout(0.1)
        # self._sock.setblocking(False)
        self._sock.bind((self._host, self._port))

        self.__receive_actions_thread: Union[threading.Thread, None] = None
        self.__do_actions_thread: Union[threading.Thread, None] = None

    def send_message(self, client_information: ClientInformation, msg: str):
        pass

    def receive_action_from_clients(self):
        # try:
        data, address = self._sock.recvfrom(self._buffer_size)
        data = data.decode()
        data = json.loads(data)
        action = Action(**data)
        self.action_queue.put((address, action))
        # except socket.timeout:
        #     pass

    def do_actions(self):
        if not self.action_queue.empty():
            address, action = self.action_queue.get()

            if action.action_type == ActionTypes.register_client:
                self.register_client(address=address, action=action)

    def register_client(self, address: str, action: Action):
        msg = Message(**action.message)
        data = json.loads(msg.message)

        client_information = ClientInformation(**data)
        client_information.ip = address
        self.connected_clients.append(client_information)
        print(self.connected_clients)

    def send_all_user_information(self, sender_information: ClientInformation):
        # self.gather_all_user_information()
        pass

    def gather_all_user_information(self):
        pass

    def _receive_actions_loop(self):
        while True:
            self.receive_action_from_clients()

    def _do_actions_loop(self):
        while True:
            self.do_actions()

    def start_receive_actions_thread(self):
        self.__receive_actions_thread = threading.Thread(target=self._receive_actions_loop)
        self.__receive_actions_thread.start()

    def start_do_actions_thread(self):
        self.__do_actions_thread = threading.Thread(target=self._do_actions_loop)
        self.__do_actions_thread.start()


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8888
    buffer_size = 1024

    master_server = MasterServer(host=host, port=port, buffer_size=buffer_size)
    print('Master server online!')
    master_server.start_receive_actions_thread()
    master_server.start_do_actions_thread()

