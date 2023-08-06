from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class GetInfoAnexos(AsteriskCommand):
    action_id: str
    action: str = "GetInfoAnexos"

    def __init__(self) -> None:
        self.is_asterisk_command = False

    def as_dict(self) -> Dict:
        return {"Action": self.action, "ActionId": self.action_id}
