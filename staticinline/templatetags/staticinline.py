import os
from logging import getLogger

from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ImproperlyConfigured
from django.template.defaulttags import register
from django.utils.safestring import mark_safe

logger = getLogger(__file__)
config = apps.get_app_config('staticinline')


@register.simple_tag()
def staticinline(path, encode=None):
    """
    Similiar to Django's native `static` templatetag, but this includes
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
    filename = None

    # Look up file in collectstatic target directory (regular deployment)
    # unless DEBUG is on. Then we skip it and lookup the file in the
    # app directory. (Thats what to expect when in DEBUG mode.)
    if not settings.DEBUG and staticfiles_storage.exists(path):
        filename = staticfiles_storage.path(path)

    # Lookup file in /app/static/ directory, e.g. when in local
    # development mode and DEBUG is True.
    if not filename:
        filename = find(path)

    # If it wasn't found, return an empty string
    # or raise ValueError if in DEBUG mode
    if not filename or not os.path.exists(filename):
        logger.error('Unable to include inline static file "%s", '
                     'file not found.', filename)
        if settings.DEBUG:
            raise ValueError('Unable to include inline static file "{0}", '
                             'file not found.'.format(filename))
        return ''

    # If we don't encode the file further, we can return it right away.
    if not encode:
        return open(filename).read()  # FIXME: Use staticfiles.open()

    encoder_registry = config.get_encoder()
    data = open(filename, 'rb').read()

    if not encode in encoder_registry:
        raise ImproperlyConfigured(
            '"{0}" is not a registered encoder. Valid values are: {1}'.format(
            encode, ', '.join(encoder_registry.keys())
        ))
    try:
        return mark_safe(encoder_registry[encode](data))
    # Anything could go wrong since we don't control the encoding
    # list itself. In case of an error raise that exception, unless
    # DEBUG mode is off. Then, same as above, return an empty string.
    except Exception as e:
        logger.error('Unable to include inline static file "%s", '
                     'file not found.', filename)
        logger.exception(e)
        if settings.DEBUG:
            raise e
    return ''


