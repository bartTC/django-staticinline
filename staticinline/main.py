from __future__ import annotations

from logging import getLogger
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage

logger = getLogger(__name__)


class FileDoesNotExistError(FileNotFoundError):
    pass


def read_static_file(path: str, mode: str = "r") -> str:
    """
    Return the contents of a static file.
    """
    if settings.DEBUG:
        # Lookup file in using Django's static finder,
        # e.g. when in local development mode.
        filename = find(path)
        if filename:
            with Path(filename).open(mode=mode) as f:
                return f.read()
    elif staticfiles_storage.exists(path):
        # Look up file in collectstatic target directory (regular
        # deployment).
        return staticfiles_storage.open(path, mode=mode).read()

    message = 'Unable to include inline static file "%s", file not found.'
    logger.warning(message, path)
    raise FileDoesNotExistError(message % path)
