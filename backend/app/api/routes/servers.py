from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request

from ...data.models.responses import BaseResponse
from ...data.models.server import ServerConfigurationResponse, ServerOption
from ...services.server import ServerService
from ..dependencies import get_server_service2

router = APIRouter()


def extract_configuration(request: Request) -> Dict[str, str]:
    """Extract server configuration from query parameters."""
    _configuration = {
        key: value
        for key, value in request.query_params.items()
        if value and value.strip()
    }
    return _configuration


@router.get("/configure", response_model=BaseResponse[ServerConfigurationResponse])
async def get_server_configuration(
    request: Request,
    service: ServerService = Depends(get_server_service2),
) -> BaseResponse[ServerConfigurationResponse]:
    try:
        configuration = extract_configuration(request)
        result = service.get_server_configuration(configuration)
        return BaseResponse.success(
            message="Server configuration validated successfully.",
            data=result
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/options", response_model=BaseResponse[Dict[str, List[ServerOption]]])
async def get_server_options(
        service: ServerService = Depends(get_server_service2),
):
    options = service.get_server_options()
    return BaseResponse.success(
        message="Server options retrieved successfully.",
        data=options
    )
