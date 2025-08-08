import re
from os import path

from .core.exceptions import PackageVersionNotFoundError
from .core.settings import settings


def _get_version() -> str:
    with open(f"{path.join(settings.BASE_DIR, 'pyproject.toml')}") as f:
        for line in f:
            match = re.match(r'version\s*=\s*"(.*)"', line)
            if match:
                return match.group(1)
    raise PackageVersionNotFoundError("Version not found in pyproject.toml")


__version__ = _get_version()
