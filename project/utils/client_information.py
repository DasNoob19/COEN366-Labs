from dataclasses import dataclass
from ipaddress import ip_address
from typing import Union, Tuple

from .file_lst import FileLst


@dataclass
class ClientInformation:
    name: str
    ip: Union[Tuple[str, int], None]  # This is None when on the client side, and client_address type on the master side
    master_address: ip_address
    tcp_file_sharing_port: int
    file_lst: FileLst
    # ack_receiver_port: int
