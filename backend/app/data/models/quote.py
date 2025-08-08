from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field


class Quote(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    configuration: dict[str, str]
    contact_name: str
    contact_email: EmailStr
    company: Optional[str] = None
    total_price: Decimal
    total_discount: Optional[Decimal] = None
    created_at: datetime = Field(default_factory=datetime.now)

class QuoteRequest(BaseModel):
    configuration: dict[str, str]
    contact_name: str
    contact_email: EmailStr
    company: Optional[str] = None

class QuoteResponse(BaseModel):
    id: str
    total_price: Decimal
    created_at: datetime
