from typing import Any, Dict, List, NamedTuple

from ...data.models import Rule
from .base import RuleHandler


class ValidationResult(NamedTuple):

    is_valid: bool
    error_messages: List[str]


class ValidationHandler(RuleHandler):
    """Handler for validation rule processing."""

    def can_handle(self, rule_type: str) -> bool:
        return rule_type == "validation"

    def execute(self, rules: List[Rule], context: Any) -> ValidationResult:
        """Execute validation rules - collect all errors."""
        all_errors = []

        for rule in rules:
            errors = self._execute_validation_action(rule, context)
            all_errors.extend(errors)

        return ValidationResult(
            is_valid=len(all_errors) == 0, error_messages=all_errors
        )

    @staticmethod
    def _execute_validation_action(rule: Rule, _:  Dict[str, str]
    ) -> List[str]:
        """Execute a single validation rule action."""
        action_type = rule.actions.get("type")

        if action_type == "add_error":
            message = rule.actions.get("message", "Validation error")
            return [message]

        return []
