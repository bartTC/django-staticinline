from __future__ import absolute_import
from logging import getLogger

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.defaulttags import register
from django.utils.safestring import mark_safe

from staticinline.main import read_static_file

logger = getLogger(__file__)
config = apps.get_app_config('staticinline')


@register.simple_tag()
def staticinline(path, encode=None):
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

    Raises a ValueError if the the file does not exist, and
    DEBUG is enabled.

    :param str path: Filename of the file to include.
    :return: Returns the the file content *or* ``''`` (empty string) if the
        file was not found, and ``DEBUG`` is ``False``.
    :rtype: str
    :raises ValueError: if the file is not found and ``DEBUG`` is ``True``
    """
    try:
        data = read_static_file(path, mode='rb' if encode else 'r')
    except ValueError:
        if settings.DEBUG:
            raise
        return ''

    # If we don't encode the file further, we can return it right away.
    if not encode:
        return mark_safe(data)

    encoder_registry = config.get_encoder()

    if encode not in encoder_registry:
        raise ImproperlyConfigured(
            '"{0}" is not a registered encoder. Valid values are: {1}'.format(
                encode, ', '.join(encoder_registry.keys())
            )
        )
    try:
        return mark_safe(encoder_registry[encode](data))
    # Anything could go wrong since we don't control the encoding
    # list itself. In case of an error raise that exception, unless
    # DEBUG mode is off. Then, same as above, return an empty string.
    except Exception as e:
        logger.error(
            'Error encoding to data format %s in static file "%s".',
            encode, path)
        logger.exception(e)
        if settings.DEBUG:
            raise e
    return ''
