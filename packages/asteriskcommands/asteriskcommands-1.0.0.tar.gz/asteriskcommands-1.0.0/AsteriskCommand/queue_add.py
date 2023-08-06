from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class QueueAdd(AsteriskCommand):
    action_id: str
    queue: str
    interface: str
    penalty: str
    paused: str
    member_name: str
    state_interface: str
    action: str = "QueueAdd"

    def as_dict(self) -> Dict:
        return {
            "Action": self.action,
            "ActionID": self.action_id,
            "Queue": self.queue,
            "Interface": self.interface,
            "Penalty": self.penalty,
            "Paused": self.paused,
            "MemberName": self.member_name,
            "StateInterface": self.state_interface,
        }
