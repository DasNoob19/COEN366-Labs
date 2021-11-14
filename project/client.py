import json
import socket
from ipaddress import ip_address
import dataclasses

from utils.message import Message
from utils.file_lst import FileLst
from utils.client_information import ClientInformation
from utils.action import Action, ActionTypes


class Client:
    def __init__(
            self,
            master_server_address: ip_address,
            master_server_port: int,
            receiver_port: ip_address,
            tcp_sender: ip_address,
            file_lst: FileLst = None
    ):
        self.master_server_address: ip_address = master_server_address
        self.master_server_port: int = master_server_port
        self._master_server_information = (self.master_server_address, self.master_server_port)

        self.receiver_port: ip_address = receiver_port  # from the client itself/is this the self address?
        self.tcp_sender: ip_address = tcp_sender
        self.file_lst: FileLst = file_lst

        self.name = socket.gethostname()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _request_master_for_action(self, action: Action):  # Logic for UDP Communication
        action = dataclasses.asdict(action)
        print(action)
        action = json.dumps(action).encode()

        self._socket.sendto(action, self._master_server_information)

    def register_with_master_server(self):
        # Send it's information to the master server
        self_information = ClientInformation(
            master_address=self.master_server_address,
            file_lst=self.file_lst,
            tcp_file_sharing_port=self.receiver_port,
            ip=None,
            name=self.name
        )

        msg = json.dumps(dataclasses.asdict(self_information))
        msg = Message(message=msg)
        action = Action(ActionTypes.register_client, message=msg)

        self._request_master_for_action(action)

    def send_updates_to_master_server(self, msg: Message):
        pass

    def send_file(self, file_name, sender_address: str):
        pass


if __name__ == '__main__':
    master_server_address = '192.168.1.2'
    master_server_port = 8888
    receiver_port = 8889
    tcp_sender = 8787

    client = Client(
        master_server_address=master_server_address,
        master_server_port=master_server_port,
        file_lst=FileLst(),
        tcp_sender=tcp_sender,
        receiver_port=receiver_port
    )

    client.register_with_master_server()
