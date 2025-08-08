from decimal import Decimal
from typing import Any, Dict, List, Tuple

from ...data.models import Rule
from .base import RuleHandler


class DiscountHandler(RuleHandler):

    def __init__(self, data_provider):
        self.data_provider = data_provider

    def can_handle(self, rule_type: str) -> bool:
        return rule_type == "discount"

    def execute(self, rules: List[Rule], context: Any) -> Tuple[Decimal, List[str]]:
        """Execute discount rules - additive accumulation."""
        total_discount = Decimal("0")
        descriptions = []

        for rule in rules:
            amount, description = self._execute_discount_action(rule, context)
            if amount > 0:
                total_discount += amount
                descriptions.append(description)

        return total_discount, descriptions

    def _execute_discount_action(
        self, rule: Rule, configuration: Dict[str, str]
    ) -> Tuple[Decimal, str]:
        """Execute a single discount rule action."""
        action_type = rule.actions.get("type")

        if action_type == "percentage_discount":
            category_id = rule.actions.get("category")
            percentage = Decimal(rule.actions.get("percentage", "0"))
            description = rule.actions.get("description", "")

            # Get the option ID for this category
            option_id = configuration.get(category_id)
            if option_id:
                # Get option price from the data provider
                option_price = self.data_provider.get_option_price(option_id)
                if option_price > 0:
                    discount_amount = option_price * (percentage / 100)
                    return discount_amount, description

        return Decimal("0"), ""
