import os
from logging import getLogger

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.defaulttags import register
from django.utils.safestring import mark_safe

logger = getLogger(__file__)


@register.simple_tag()
def staticinline(path):
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

    return mark_safe(open(filename).read())
