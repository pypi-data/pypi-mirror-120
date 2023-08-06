from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class Redirect(AsteriskCommand):
    channel: str
    context: str
    exten: str
    priority: str
    action_id: str
    peer_name: str
    action: str = "Redirect"

    def as_dict(self) -> Dict:
        return {
            "Action": self.action,
            "Channel": self.channel,
            "Context": self.context,
            "Exten": self.exten,
            "Priority": self.priority,
            "ActionID": self.action_id,
            "peerName": self.peer_name,
        }
