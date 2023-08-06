from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class GetAgentStatus(AsteriskCommand):
    action_id: str
    interface: str
    action: str = "GetAgentStatus"

    def __init__(self) -> None:
        self.is_asterisk_command = False

    def as_dict(self) -> Dict:
        return {
            "Action": self.action,
            "ActionID": self.action_id,
            "Interface": self.interface,
        }
