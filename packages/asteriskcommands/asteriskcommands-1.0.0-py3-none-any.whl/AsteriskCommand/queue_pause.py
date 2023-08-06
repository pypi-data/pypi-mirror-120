from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class QueuePause(AsteriskCommand):
    transaction_id: str
    queue: str
    action_id: str
    interface: str
    paused: str
    reason: str
    member_name: str
    action: str = "QueuePause"

    def as_dict(self) -> Dict:
        return {
            "Action": self.action,
            "ActionID": self.transaction_id,
            "Queue": self.queue,
            "Interface": self.interface,
            "Paused": self.paused,
            "Reason": self.reason,
            "MemberName": self.member_name,
        }
