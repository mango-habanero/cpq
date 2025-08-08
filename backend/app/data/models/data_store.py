from decimal import Decimal
from typing import Dict, Optional

from pydantic import BaseModel, Field


class Category(BaseModel):

    id: str
    name: str
    description: str
    required: bool
    order: int


class Option(BaseModel):

    id: str
    category_id: str
    display_name: str
    price: Decimal
    available: bool
    order: int


class Rule(BaseModel):

    id: str
    name: str
    type: str
    conditions: Dict
    actions: Dict
    priority: int
    active: bool


class Setting(BaseModel):

    key: str
    value: str
    description: str


class RuleContext(BaseModel):
    configuration: Dict[str, str] = Field(default_factory=dict)
    current_option: Optional[Option] = None
