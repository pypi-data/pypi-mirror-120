from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class Originate(AsteriskCommand):
    action_id: str
    channel: str
    context: str
    exten: str
    priority: str
    callerid: str
    timeout: str
    action: str = "Originate"

    def as_dict(self) -> Dict:
        return {
            "Action": self.action,
            "ActionID": self.action_id,
            "Channel": self.channel,
            "Context": self.context,
            "Exten": self.exten,
            "Priority": self.priority,
            "Callerid": self.callerid,
            "Timeout": self.timeout,
            "Variables": self.variables,
        }
