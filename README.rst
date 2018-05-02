.. image:: https://travis-ci.org/bartTC/django-staticinline.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-staticinline

.. image:: https://api.codacy.com/project/badge/Coverage/8e64345e99ea49888dc1bd9303c89a35
    :target: https://www.codacy.com/app/bartTC/django-staticinline?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bartTC/django-staticinline&amp;utm_campaign=Badge_Coverage

.. image:: https://api.codacy.com/project/badge/Grade/8e64345e99ea49888dc1bd9303c89a35
    :target: https://www.codacy.com/app/bartTC/django-staticinline?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bartTC/django-staticinline&amp;utm_campaign=Badge_Grade

===================
django-staticinline
===================

Similiar to Django's native ``static`` templatetag, but this includes
the file directly in the template, rather than a link to it.

Example:

.. code:: jinja

    {% load staticinline %}

    <style type="text/css">{% staticinline "myfile.css" %}</style>
    <script>{% staticinline "myfile.js" %}</script>

Becomes:

.. code:: html

    <style type="text/css">body{ color: red; }</style>
    <script>alert("Hello World");</script>

If the file does not exist, and ``DEBUG`` is ``False``, an empty string
is returned and a error logfile is set. In case ``DEBUG`` is ``True``,
a ``ValueError`` is raised.

Installation
============

This Django app is compatible with Django 1.8 → 2.0, Python 2.7 all
versions of Python 3.x.

Install the app with pip and add ``staticinline.apps.StaticInlineAppConfig``
to your installed apps in your settings.py:

.. code:: text

    pip install django-staticinline

.. code:: python

    INSTALLED_APPS = [
        # ...
        'staticinline.apps.StaticInlineAppConfig',
    ]

Encoder and Customization
=========================

You can automatically convert the file with the ``encode`` argument.
django-staticinline ships with one encoder, ``base64`` that transforms
the file content to a base64 encoded string.

Usage:


.. code:: jinja

    {% load staticinline %}
    {% staticinline "mykey.pem" encode="base64" %}'

Becomes:

.. code:: text

    LS0tIFN1cGVyIFByaXZhdGUgS2V5IC0tLQo=

You can add custom filter by setting them in a custom AppConfig.
See the default AppConfig in ``staticinline/apps.py`` for further documentation.
The testsuite also uses a custom AppConfig, which will help you to understand
the setup. See ``staticinline/tests/testapp/apps.py`` for it.
