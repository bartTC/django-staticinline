.. _installation:

====================
Installation & Usage
====================

Install the app with pip and add ``staticinline.apps.StaticInlineAppConfig``
to your installed apps in your settings.py:

.. code:: text

    pip install django-staticinline

.. code:: python

    INSTALLED_APPS = [
        # ...
        'staticinline.apps.StaticInlineAppConfig',
    ]

In a Django template load the ``staticinline`` templatetag and load
a file using the same tag just as you'd load a file with the regular
``static`` templatetag.

.. code:: django

    {% load staticinline %}

    <style type="text/css">{% staticinline "myfile.css" %}</style>
    <script>{% staticinline "myfile.js" %}</script>

.. note::
    If the file does not exist, and ``DEBUG`` is ``False``, an empty string
    is returned and a error logfile is set. In case ``DEBUG`` is ``True``,
    a ``ValueError`` is raised.



Caching
=======

You can optioanlly cache the file content. This is particularly useful if you
use expensive encoder processing.

Pass the ``cache=True`` argument. Additionally you can pass a timeout
(in seconds) using the ``cache_timeout`` argument. If not set, the default
timeout defined in the AppConfig is used.

.. code:: django

    {% load staticinline %}

    {% staticinline "mykey.pem" encode="base64" cache=True %}
    {% staticinline "mykey.pem" encode="base64" cache=True cache_timeout=3600 %}
