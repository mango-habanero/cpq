from fastapi import APIRouter, Depends, HTTPException

from ...data.models.quote import QuoteRequest, QuoteResponse
from ...data.models.responses import BaseResponse
from ...services.quote import QuoteService
from ..dependencies import get_quote_service

router = APIRouter()


@router.post("/requests", response_model=BaseResponse[QuoteResponse], status_code=201)
async def create_quote_request(
    request: QuoteRequest, service: QuoteService = Depends(get_quote_service)
) -> BaseResponse[QuoteResponse]:
    try:
        quote = service.create_quote(request)
        return BaseResponse.success(
            message="Quote request created successfully.", data=quote
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
