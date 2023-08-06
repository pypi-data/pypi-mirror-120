from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class SIPpeers(AsteriskCommand):
    action_id: str
    action: str = "SIPpeers"

    def as_dict(self) -> Dict:
        return {"Action": self.action, "ActionID": self.action_id}
