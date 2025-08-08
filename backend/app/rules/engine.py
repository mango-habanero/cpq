from typing import Any

from ..core.logger import app_logger
from ..data import DataProvider
from ..data.models import RuleContext
from ..rules.handlers import HandlerRegistry
from .condition_evaluator import ConditionEvaluator


class RulesEngine:

    def __init__(self, data_provider: DataProvider, handler_registry: HandlerRegistry):
        self.data_provider = data_provider
        self.handler_registry = handler_registry
        self.condition_evaluator = ConditionEvaluator()

    def process_rules(self, rule_type: str, context: RuleContext) -> Any:
        rules = self.data_provider.get_rules_by_type(rule_type)

        matching_rules = [
            rule
            for rule in rules
            if self.condition_evaluator.matches_conditions(rule.conditions, context)
        ]

        app_logger.debug(f"Processing {len(matching_rules)} matching rules for type '{rule_type}'")

        handler = self.handler_registry.get_handler(rule_type)
        if not handler:
            raise ValueError(f"No handler registered for rule type: {rule_type}")

        try:
            return handler.execute(matching_rules, context)
        except Exception:
            app_logger.exception(f"Handler execution failed for rule type '{rule_type}'")
            raise

    def add_handler(self, rule_type: str, handler) -> None:
        self.handler_registry.register_handler(rule_type, handler)


def initialize_rule_engine(
    data_provider: DataProvider,
    handler_registry: HandlerRegistry
) -> RulesEngine:
    app_logger.debug("Initializing rule engine")
    return RulesEngine(data_provider, handler_registry)
