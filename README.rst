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

.. code:: django

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
django-staticinline ships with two encoders: ``base64`` that transforms the
file content to a base64 encoded string, and ``data`` that transforms the
content into a data URI for use in CSS ``url()`` and HTML ``src=""``
attributes.

``base64`` encoder
------------------

.. code:: django

    {% load staticinline %}
    {% staticinline "mykey.pem" encode="base64" %}'

Becomes:

.. code:: text

    LS0tIFN1cGVyIFByaXZhdGUgS2V5IC0tLQo=

``data`` encoder
----------------

.. code:: css+django

    {% load staticinline %}
    ul.checklist li.complete {
        background: url('{% staticinline "icons/check.png" encode="data" %}');
    }

Becomes:

.. code:: css

    ul.checklist li.complete {
        background: url('data:image/png;base64,iVBORw0KG\
    goAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABlBMVEUAAAD//\
    /+l2Z/dAAAAM0lEQVR4nGP4/5/h/1+G/58ZDrAz3D/McH8yw83ND\
    DeNGe4Ug9C9zwz3gVLMDA/A6P9/AFGGFyjOXZtQAAAAAElFTkSuQ\
    mCC');
    }

Custom filters
--------------

You can add custom filters by setting them in a custom AppConfig. See the
default AppConfig in ``staticinline/apps.py`` for further documentation. The
test suite also uses a custom AppConfig, which will help you to understand the
setup. See ``staticinline/tests/testapp/apps.py`` for it.
