from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, cast

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from backend.app.data.provider import DataProvider, initialize_data_provider

from ..api import api_router
from ..api.health import router as health_router
from ..middleware.requests import HttpRequestLoggingMiddleware
from ..rules import RulesEngine, initialize_rule_engine
from ..rules.handlers import initialize_handler_registry
from .exceptions.handler import (
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from .settings import settings


class AppState:
    data_provider: DataProvider
    rule_engine: RulesEngine

class CPQFastAPI(FastAPI):
    @property
    def state(self) -> AppState:
        return cast(AppState, super().state)


@asynccontextmanager
async def lifespan(app: CPQFastAPI) -> AsyncIterator[None]:
    """Application lifespan context manager with enhanced error reporting."""
    data_provider = initialize_data_provider()
    handler_registry = initialize_handler_registry(data_provider)
    rule_engine = initialize_rule_engine(data_provider, handler_registry)

    app.state.data_provider = data_provider
    app.state.rule_engine = rule_engine

    yield

def create_app(
    *,
    title: str = "FastAPI",
    description: str = "",
    version: str,
    **kwargs: Any,
) -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=title,
        description=description,
        lifespan=lifespan,
        version=version,
        **kwargs,
    )
    configure_exception_handlers(app)
    configure_middleware(app)
    configure_routes(app)
    return app


def configure_middleware(app: FastAPI):
    app.add_middleware(HttpRequestLoggingMiddleware)
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )


def configure_routes(app: FastAPI):
    app.include_router(health_router)
    app.include_router(api_router, prefix="/api/v1")


def configure_exception_handlers(app: FastAPI) -> FastAPI:
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    return app
