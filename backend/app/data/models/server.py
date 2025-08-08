from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ServerOption(BaseModel):

    id: str
    display_name: str
    price: Decimal
    available: bool = True


class ServerConfigurationResponse(BaseModel):

    current_selection: dict[str, str] = Field(default_factory=dict)
    total_price: Decimal
    total_discount: Optional[Decimal] = None
    discount_descriptions: list[str] = []
    is_valid: bool = True
