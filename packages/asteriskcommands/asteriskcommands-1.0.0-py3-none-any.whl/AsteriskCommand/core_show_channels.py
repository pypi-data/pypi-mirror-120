from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class CoreShowChannels(AsteriskCommand):
    action_id: str
    action: str = "CoreShowChannels"

    def as_dict(self) -> Dict:
        return {"Action": self.action, "ActionID": self.action_id}
