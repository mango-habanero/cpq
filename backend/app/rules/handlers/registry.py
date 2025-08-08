from typing import Dict, List, Optional

from backend.app.data.provider import DataProvider

from ...core.logger import app_logger
from .availability import AvailabilityHandler
from .base import RuleHandler
from .discount import DiscountHandler
from .validation import ValidationHandler


class HandlerRegistry:

    def __init__(self):
        self._handlers: Dict[str, RuleHandler] = {}

    def register_handler(self, rule_type: str, handler: RuleHandler) -> None:
        self._handlers[rule_type] = handler

    def get_handler(self, rule_type: str) -> Optional[RuleHandler]:
        return self._handlers.get(rule_type)

    def get_supported_types(self) -> List[str]:
        return list(self._handlers.keys())


def initialize_handler_registry(data_provider: DataProvider) -> HandlerRegistry:
    try:
        app_logger.debug("Initializing handler registry")
        registry = HandlerRegistry()
        registry.register_handler("availability", AvailabilityHandler())
        registry.register_handler("discount", DiscountHandler(data_provider))
        registry.register_handler("validation", ValidationHandler())
        return registry
    except Exception as e:
        app_logger.exception("Failed to initialize handler registry")
        raise RuntimeError("Failed to initialize handler registry") from e
