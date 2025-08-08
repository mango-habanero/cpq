from pathlib import Path

from ..core.settings import Settings


def data_file(filename: str) -> Path:
    return Settings.BASE_DIR / "app" / "data" / "store" / filename
