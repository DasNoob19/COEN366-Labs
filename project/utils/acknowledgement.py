from dataclasses import dataclass
from datetime import datetime

DATETIME_FORMAT = "%m/%d/%Y, %H:%M:%S"

@dataclass
class Acknowledgement:
    timestamp: datetime = datetime.now().strftime(DATETIME_FORMAT)
