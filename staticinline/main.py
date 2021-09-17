from logging import getLogger

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage

logger = getLogger(__file__)


def read_static_file(path, mode="r"):
    """
    Return the contents of a static file.
    """
    if settings.DEBUG:
        # Lookup file in using Django's static finder, e.g. when in
        # local development mode.
        filename = find(path)
        if filename:
            return open(filename, mode=mode).read()
    elif staticfiles_storage.exists(path):
        # Look up file in collectstatic target directory (regular
        # deployment).
        return staticfiles_storage.open(path, mode=mode).read()

    message = 'Unable to include inline static file "%s", file not found.'
    logger.warning(message, path)
    raise ValueError(message % path)
