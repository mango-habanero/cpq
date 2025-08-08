from abc import ABC, abstractmethod
from typing import Any, List

from backend.app.data.models.data_store import Rule


class RuleHandler(ABC):

    @abstractmethod
    def can_handle(self, rule_type: str) -> bool:
        pass

    @abstractmethod
    def execute(self, rules: List[Rule], context: Any) -> Any:
        pass
