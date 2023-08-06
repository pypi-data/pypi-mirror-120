from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class SetVar(AsteriskCommand):
    transaction_id: str
    channel: str
    variable: str
    value: str
    action: str = "SetVar"

    def as_asterisk_command(self) -> Dict:
        return {
            "Action": self.action,
            "ActionID": self.transaction_id,
            "Channel": self.channel,
            "Variable": self.variable,
            "Value": self.value,
        }
