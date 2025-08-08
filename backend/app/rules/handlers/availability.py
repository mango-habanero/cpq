from typing import Any, List

from ...data.models import Rule
from .base import RuleHandler


class AvailabilityHandler(RuleHandler):

    def can_handle(self, rule_type: str) -> bool:
        return rule_type == "availability"

    def execute(self, rules: List[Rule], context: Any) -> bool:
        for rule in rules:
            if not self._execute_availability_action(rule, context):
                return False
        return True

    @staticmethod
    def _execute_availability_action(rule: Rule, _: tuple) -> bool:
        action_type = rule.actions.get("type")

        if action_type == "set_unavailable":
            return False

        return True
