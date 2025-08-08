from typing import Any, Dict

from ..data.models import RuleContext


class ConditionEvaluator:
    """Evaluates rule conditions against a rule context."""

    def matches_conditions(
        self, rule_conditions: Dict[str, Any], context: RuleContext
    ) -> bool:
        if not rule_conditions:
            return True

        for field_name, expected_values in rule_conditions.items():
            if not self._matches_field_condition(field_name, expected_values, context):
                return False

        return True

    def _matches_field_condition(
        self, field_name: str, expected_values: list, context: RuleContext
    ) -> bool:
        if field_name == "missing_categories":
            return self._check_missing_categories(expected_values, context.configuration)

        if field_name == "option_category":
            if context.current_option is None:
                return False
            return context.current_option.category_id in expected_values

        if field_name == "option_values":
            if context.current_option is None:
                return False
            return context.current_option.id in expected_values

        current_value = context.configuration.get(field_name)
        if current_value is None:
            return False

        return current_value in expected_values

    @staticmethod
    def _check_missing_categories(
        required_categories: list, configuration: Dict[str, str]
    ) -> bool:
        for category in required_categories:
            field_value = configuration.get(category)
            if field_value is None:
                return True
        return False
