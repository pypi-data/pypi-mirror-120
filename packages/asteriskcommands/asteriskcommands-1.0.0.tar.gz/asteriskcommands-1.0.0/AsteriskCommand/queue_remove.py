from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class QueueRemove(AsteriskCommand):
    action_id: str
    queue: str
    interface: str
    action: str = "QueueRemove"

    def as_dict(self) -> Dict:
        return {
            "Action": self.action,
            "ActionID": self.action_id,
            "Queue": self.queue,
            "Interface": self.interface,
        }
