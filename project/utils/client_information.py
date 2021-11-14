from dataclasses import dataclass
from ipaddress import ip_address
from typing import Union

from .file_lst import FileLst


@dataclass
class ClientInformation:
    name: str
    ip: Union[ip_address, None]  # This is None when on the client side, and ip_address type on the master side
    master_address: ip_address
    tcp_file_sharing_port: int
    file_lst: FileLst
