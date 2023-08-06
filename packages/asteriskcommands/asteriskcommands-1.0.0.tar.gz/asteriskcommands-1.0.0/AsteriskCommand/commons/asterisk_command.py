import json
from abc import ABC, abstractmethod
from typing import Dict, List
from AsteriskCommand.commons.asterisk_action import Action


class AsteriskCommand(ABC):
    action: str
    auxiliar_commands: List
    variables: Dict = dict()
    is_asterisk_command: bool = True

    @abstractmethod
    def as_dict(self) -> Dict:
        raise NotImplementedError("Method not implemented")

    def as_json_asterisk_command(self) -> str:
        return json.dumps(self.as_dict())

    def as_asterisk_command(self) -> Action:
        return Action(name=self.action, keys=self.as_dict(), variables=self.variables)
