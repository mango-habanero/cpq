from functools import lru_cache

from fastapi import Request

from ..rules import RulesEngine
from ..services.quote import QuoteService
from ..services.server import ServerService


@lru_cache()
def get_quote_service(request: Request) -> QuoteService:
    """Get cached quote service."""
    return QuoteService(server_service=get_server_service2(request))


def get_rule_engine(request: Request) -> RulesEngine:
    """Retrieve the pre-configured RulesEngine from app state.

    This is the ONLY dependency that needs to be retrieved from app state,
    as it's initialized once during application startup.
    """
    return request.app.state.rule_engine


@lru_cache()
def get_server_service2(request: Request) -> ServerService:
    """Get cached server service."""
    return ServerService(rule_engine=get_rule_engine(request))

