from __future__ import annotations

from logging import getLogger

from django.apps import apps
from django.conf import settings
from django.core.cache import cache as cache_backend
from django.core.exceptions import ImproperlyConfigured
from django.template.defaulttags import register

from staticinline.main import read_static_file

logger = getLogger(__name__)
config = apps.get_app_config("staticinline")


@register.simple_tag()
def staticinline(  # noqa: C901 Too Complex
    path: str,
    encode: str | None = None,
    cache: bool = False,
    cache_timeout: bool | None = None,
) -> str:
    """
    Similar to Django's native `static` templatetag, but this includes
    the file directly in the template, rather than a link to it.

    Example::

    {% load staticinline %}

    <style type="text/css">{% staticinline "myfile.css" %}</style>
    <script>{% staticinline "myfile.js" %}</script>

    Becomes::

        <style type="text/css">body{ color: red; }</style>
        <script>alert("Hello World");</script>

    Raises a ValueError if the file does not exist, and DEBUG is enabled.

    :param str path: Filename of the file to include.
    :param str encode: Custom encoder function to run on data.
    :param bool cache: Whether to cache the response.
    :param int cache_timeout: The cache timeout for this particular file.
        If not set, AppConfig.cache_timeout is used.
    :return: Returns the file content *or* ``''`` (empty string) if the
        file was not found, and ``DEBUG`` is ``False``.
    :rtype: str
    :raises ValueError: if the file is not found and ``DEBUG`` is ``True``
    """
    cache_key = None
    cache_timeout = cache_timeout or config.cache_timeout

    # Retrieve from cache if set
    if cache:
        cache_key = config.build_cache_key(path, encode)
        cached_obj = cache_backend.get(cache_key)
        logger.debug("Cache enabled, cache key: %s", cache_key)

        if cached_obj:
            logger.debug("Object found in cache")
            return config.data_response(cached_obj)

    try:
        data = read_static_file(path, mode="rb" if encode else "r")
    except FileNotFoundError:
        if settings.DEBUG:
            raise
        return ""

    # If we don't encode the file further, we can return it right away.
    if not encode:
        if cache:
            cache_backend.set(cache_key, data, cache_timeout)
            logger.debug("Object set in cache, cache key: %s", cache_key)
        return config.data_response(data)

    encoder_registry = config.get_encoder()

    if encode not in encoder_registry:
        msg = '"{}" is not a registered encoder. Valid values are: {}'.format(
            encode,
            ", ".join(encoder_registry.keys()),
        )
        raise ImproperlyConfigured(msg)
    try:
        response = encoder_registry[encode](data, path)
        if cache:
            logger.debug("Object encoded and set in cache, cache key: %s", cache_key)
            timeout = cache_timeout or config.cache_timeout
            cache_backend.set(cache_key, response, timeout)
        return config.data_response(response)

    # Anything could go wrong since we don't control the encoding
    # list itself. In case of an error raise that exception, unless
    # DEBUG mode is off. Then, same as above, return an empty string.
    except Exception:
        logger.exception(
            'Error encoding to data format %s in static file "%s".', encode, path
        )
        if settings.DEBUG:
            raise

    return ""
