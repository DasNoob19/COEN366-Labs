from typing import Union, Dict
from dataclasses import dataclass
from enum import Enum, auto

from .message import Message


class ActionTypes(int, Enum):
    register_client = auto()


@dataclass
class Action:
    action_type: ActionTypes
    message: Union[Message, Dict]
