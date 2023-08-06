from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class Atxfer(AsteriskCommand):
    action_id: str
    channel: str
    context: str
    exten: str
    priority: str
    peer_name: str
    action: str = "Atxfer"

    def as_dict(self) -> Dict:
        return {
            "Action": self.action,
            "ActionID": self.action_id,
            "Channel": self.channel,
            "Context": self.context,
            "Exten": self.exten,
            "Priority": self.priority,
            "peerName": self.peer_name,
        }
