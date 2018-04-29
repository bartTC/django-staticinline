===================
django-staticinline
===================

Similiar to Django's native `static` templatetag, but this includes
the file directly in the template, rather than a link to it.

Example::

    {% load staticinline %}

    <style type="text/css">{% staticinline "myfile.css" %}</style>
    <script>{% staticinline "myfile.js" %}</script>

Becomes::

    <style type="text/css">body{ color: red; }</style>
    <script>alert("Hello World");</script>

If the file does not exist, and ``DEBUG`` is ``False``, an empty string
is returned and a error logfile is set. In case ``DEBUG`` is ``True``,
a ``ValueError`` is raised.

Installation
============

This Django app is compatible with Django 1.8 → 2.0, Python 2.7 all
versions of Python 3.x.

Install with pip and add ``staticinline`` to your installed apps in your
settings.py::

    pip install django-staticinline

    INSTALLED_APPS = [
        # ...
        'staticinline',
    ]
