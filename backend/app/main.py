#!/usr/bin/env python3
"""
Application entry point.
"""

from . import __version__
from .core.logger import configure_logging
from .core.settings import settings

configure_logging(
    enable_json_logging=settings.STRUCTURED_LOGGING_ENABLED,
    log_level=settings.LOG_LEVEL
)

from .core.app import create_app


def main():
    return create_app(
        description="A simple CPQ system demonstrating a reactive endpoint",
        title="CPQ System",
        version=__version__,
    )

app = main()
