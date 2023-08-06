from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class Hangup(AsteriskCommand):
    action_id: str
    channel: str
    peer_name: str
    action: str = "Hangup"

    def as_dict(self) -> Dict:
        return {
            "Action": self.action,
            "ActionID": self.action_id,
            "Channel": self.channel,
            "peerName": self.peer_name,
        }
