from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from ...data.enums import ResponseStatus

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):

    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True, extra="ignore"
    )

    status: ResponseStatus
    message: str
    data: Optional[T] = Field(default=None, exclude_none=True)

    @classmethod
    def success(cls, message: str, data: T) -> "BaseResponse[T]":
        return cls(status=ResponseStatus.SUCCESS, message=message, data=data)


class ErrorDetail(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    field: Optional[str] = None
    message: str
    rejected_value: Optional[str] = None

    @classmethod
    def of(
        cls, field: Optional[str], message: str, rejected_value: Optional[str] = None
    ) -> "ErrorDetail":
        return cls(field=field, message=message, rejected_value=rejected_value)


class ErrorResponse(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    status: ResponseStatus = ResponseStatus.FAILED
    code: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    errors: List[ErrorDetail] = Field(default_factory=list)
    error_reference: str = Field(default_factory=lambda: uuid4().hex)

    @classmethod
    def from_exception(
        cls,
        code: str,
        message: str,
        errors: Optional[List[ErrorDetail]] = None,
        error_reference: Optional[str] = None,
    ) -> "ErrorResponse":
        return cls(
            code=code,
            message=message,
            errors=errors or [],
            error_reference=error_reference or uuid4().hex,
        )
