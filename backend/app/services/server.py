from decimal import Decimal
from typing import List, Optional

from ..data.models import RuleContext, ServerConfigurationResponse, ServerOption
from ..rules import RulesEngine


class ServerService:
    """Service for server configuration logic using the pre-configured rules engine."""

    def __init__(self, rule_engine: RulesEngine):
        self.rule_engine = rule_engine

    def get_server_configuration(self, configuration: dict[str, str]) -> ServerConfigurationResponse:
        validation_context = RuleContext(configuration=configuration)
        validation_result = self.rule_engine.process_rules("validation", validation_context)
        if not validation_result.is_valid:
            raise ValueError("; ".join(validation_result.error_messages))

        total_price, total_discount, descriptions = self._calculate_pricing(configuration)

        return ServerConfigurationResponse(
            current_selection=configuration,
            total_price=total_price,
            total_discount=total_discount if total_discount > 0 else None,
            discount_descriptions=descriptions,
            is_valid=True,
        )

    def get_server_options(self, current_configuration: Optional[dict[str, str]] = None) -> dict[str, List[ServerOption]]:
        options_by_category = {}

        categories = self.rule_engine.data_provider.get_all_categories()

        for category in categories:
            category_options = []
            available_options = self.rule_engine.data_provider.get_available_options_by_category(category.id)

            for option in available_options:
                if current_configuration:
                    availability_context = RuleContext(
                        configuration=current_configuration,
                        current_option=option
                    )
                    is_available = self.rule_engine.process_rules("availability", availability_context)
                else:
                    is_available = option.available

                category_options.append(ServerOption(
                    id=option.id,
                    display_name=option.display_name,
                    price=option.price,
                    available=is_available,
                ))

            options_by_category[category.id] = category_options

        return options_by_category

    def _calculate_pricing(self, configuration: dict[str, str]) -> tuple[Decimal, Decimal, List[str]]:
        total = self.rule_engine.data_provider.get_base_price()

        for category_id, option_id in configuration.items():
            if option_id:
                option_price = self.rule_engine.data_provider.get_option_price(option_id)
                total += option_price

        discount_context = RuleContext(configuration=configuration)
        total_discount, descriptions = self.rule_engine.process_rules("discount", discount_context)
        final_price = total - total_discount

        return final_price, total_discount, descriptions
