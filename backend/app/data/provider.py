import json
from decimal import Decimal
from pathlib import Path

from ..core.logger import app_logger
from ..data.models import Category, Option, Rule, Setting
from ..data.utilities import data_file


class DataProvider:
    """Centralized provider for all configuration data with efficient lookups."""

    def __init__(
        self,
        categories_file: Path,
        options_file: Path,
        rules_file: Path,
        settings_file: Path,
    ) -> None:
        self.categories = self._load_categories(categories_file)
        self.options = self._load_options(options_file)
        self.rules = self._load_rules(rules_file)
        self.settings = self._load_settings(settings_file)

        self._build_indexes()

        self._validate_data()

    def get_all_categories(self) -> list[Category]:
        return sorted(self.categories, key=lambda c: c.order)

    def get_available_options_by_category(self, category_id: str) -> list[Option]:
        return [
            opt for opt in self.get_options_by_category(category_id) if opt.available
        ]

    def get_base_price(self) -> Decimal:
        """Get base server price from rules."""
        pricing_rules = self.get_rules_by_type("pricing")
        for rule in pricing_rules:
            if rule.id == "base_pricing":
                return Decimal(rule.actions.get("amount", "0.00"))
        return Decimal("0.00")

    def get_option_price(self, option_id: str) -> Decimal:
        """Get option price"""
        price = self._prices_by_option_id.get(option_id)
        if price is None:
            raise ValueError(f"Unknown option ID: {option_id}")
        return price

    def get_options_by_category(self, category_id: str) -> list[Option]:
        options = self._options_by_category.get(category_id, [])
        return sorted(options, key=lambda o: o.order)

    def get_rules_by_type(self, rule_type: str) -> list[Rule]:
        return self._active_rules_by_type.get(rule_type, [])

    def _build_indexes(self) -> None:

        self._categories_by_id = {cat.id: cat for cat in self.categories}

        self._options_by_id = {opt.id: opt for opt in self.options}
        self._options_by_category: dict[str, list[Option]] = {}
        for option in self.options:
            if option.category_id not in self._options_by_category:
                self._options_by_category[option.category_id] = []
            self._options_by_category[option.category_id].append(option)

        self._prices_by_option_id = {opt.id: opt.price for opt in self.options}

        self._rules_by_type: dict[str, list[Rule]] = {}
        self._active_rules_by_type: dict[str, list[Rule]] = {}
        for rule in self.rules:
            # - rules by type
            if rule.type not in self._rules_by_type:
                self._rules_by_type[rule.type] = []
            self._rules_by_type[rule.type].append(rule)

            # - rules by type (sorted by priority)
            if rule.active:
                if rule.type not in self._active_rules_by_type:
                    self._active_rules_by_type[rule.type] = []
                self._active_rules_by_type[rule.type].append(rule)

        # sort rules by priority (lower number = higher priority)
        for rule_type in self._active_rules_by_type:
            self._active_rules_by_type[rule_type].sort(key=lambda r: r.priority)

        # settings lookup
        self._settings_by_key = {setting.key: setting for setting in self.settings}

    def _load_categories(self, file_path: Path) -> list[Category]:
        """Load categories from the pertinent file."""
        return self._load_jsonl_file(file_path, Category, "categories")

    @staticmethod
    def _load_jsonl_file(file_path: Path, model_class, data_type: str) -> list:
        items = []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        data = json.loads(line)

                        if model_class == Option and "price" in data:
                            data["price"] = Decimal(data["price"])

                        items.append(model_class.model_validate(data))
        except FileNotFoundError:
            raise RuntimeError(f"{data_type} file not found: {file_path}")
        except (json.JSONDecodeError, ValueError) as e:
            raise RuntimeError(f"Invalid data in {data_type} file: {e}")

        return items

    def _load_options(self, file_path: Path) -> list[Option]:
        return self._load_jsonl_file(file_path, Option, "options")

    def _load_rules(self, file_path: Path) -> list[Rule]:
        return self._load_jsonl_file(file_path, Rule, "rules")

    def _load_settings(self, file_path: Path) -> list[Setting]:
        return self._load_jsonl_file(file_path, Setting, "settings")

    def _validate_data(self) -> None:
        errors = []

        category_ids = set(cat.id for cat in self.categories)
        for option in self.options:
            if option.category_id not in category_ids:
                errors.append(
                    f"Option '{option.id}' references unknown category '{option.category_id}'"
                )

        if not self.categories:
            errors.append("No categories defined")

        if not self.options:
            errors.append("No options defined")

        if errors:
            raise RuntimeError(f"Data validation failed: {'; '.join(errors)}")


def initialize_data_provider() -> DataProvider:
    try:
        app_logger.debug("Initializing data provider")
        return DataProvider(
            categories_file=data_file("categories.jsonl"),
            options_file=data_file("options.jsonl"),
            rules_file=data_file("rules.jsonl"),
            settings_file=data_file("settings.jsonl"),
        )
    except Exception as e:
        app_logger.exception("Failed to initialize DataProvider")
        raise RuntimeError("Failed to initialize DataProvider") from e
